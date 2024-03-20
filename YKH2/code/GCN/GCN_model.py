# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:08:55 2023

@author: kyoo02
"""


import os
import pandas as pd
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def create_ffn(hidden_units, dropout_rate, name=None):
    fnn_layers = []

    for units in hidden_units:
        fnn_layers.append(layers.BatchNormalization())
        fnn_layers.append(layers.Dropout(dropout_rate))
        fnn_layers.append(layers.Dense(units, activation=tf.nn.gelu))

    return keras.Sequential(fnn_layers, name=name)    

class GraphConvLayer(layers.Layer):
    def __init__(
            self,
            hidden_units,
            dropout_rate = 0.2,
            aggregation_type = "mean",
            combination_type = "concat",
            normalize = False,
            *arg,
            **kwargs
            ):
        super().__init__(*arg, **kwargs)
        
        self.aggregation_type = aggregation_type
        self.combination_type = combination_type
        self.normalize        = normalize
        
        self.ffn_prepare = create_ffn(hidden_units, dropout_rate)
        if self.combination_type == "gated":
            self.update_fn = layers.GRU(
                units = hidden_units,
                activation = "tanh",
                recurrent_activation = "sigmoid",
                dropout = dropout_rate,
                return_state = True,
                recurrent_dropout = dropout_rate,
                )
        else:
            self.update_fn = create_ffn(hidden_units, dropout_rate)

    def prepare(self, node_representations, weights=None):
        messages = self.ffn_prepare(node_representations)
        if weights is not None:
            messages = messages * tf.expand_dims(weights, -1)
        return messages
    
    def aggregate(self, node_indices, neighbour_messages, node_representations):
        num_nodes = node_representations.shape[0]
        if self.aggregation_type == "sum":
            aggregated_message = tf.math.unsorted_segment_sum(
                neighbour_messages, node_indices, num_segments=num_nodes
                )
        elif self.aggregation_type == "mean":
            aggregated_message = tf.math.unsorted_segment_mean(
                neighbour_messages, node_indices, num_segments=num_nodes
            )
        elif self.aggregation_type == "max":
            aggregated_message = tf.math.unsorted_segment_max(
                neighbour_messages, node_indices, num_segments=num_nodes
            )
        else:
            raise ValueError(f"Invalid aggregation type: {self.aggregation_type}.")
        return aggregated_message
    
    def update(self, node_representations, aggregated_messages):
        if self.combination_type == "gru":
            h = tf.stack([node_representations, aggregated_messages], axis=1)
        elif self.combination_type == "concat":
            h = tf.concat([node_representations, aggregated_messages], axis=1)
        elif self.combination_type == "add":
            # Add node_repesentations and aggregated_messages.
            h = node_representations + aggregated_messages
        else:
            raise ValueError(f"Invalid combination type: {self.combination_type}.")

        # Apply the processing function.
        node_embeddings = self.update_fn(h)
        if self.combination_type == "gru":
            node_embeddings = tf.unstack(node_embeddings, axis=1)[-1]

        if self.normalize:
            node_embeddings = tf.nn.l2_normalize(node_embeddings, axis=-1)
        return node_embeddings

    def call(self, inputs):
        """Process the inputs to produce the node_embeddings.

        inputs: a tuple of three elements: node_repesentations, edges, edge_weights.
        Returns: node_embeddings of shape [num_nodes, representation_dim].
        """

        node_repesentations, edges, edge_weights = inputs
        # Get node_indices (source) and neighbour_indices (target) from edges.
        node_indices, neighbour_indices = edges[0], edges[1]
        # neighbour_repesentations shape is [num_edges, representation_dim].
        neighbour_repesentations = tf.gather(node_repesentations, neighbour_indices)

        # Prepare the messages of the neighbours.
        neighbour_messages = self.prepare(neighbour_repesentations, edge_weights)
        # Aggregate the neighbour messages.
        aggregated_messages = self.aggregate(
            node_indices, neighbour_messages, node_repesentations
        )
        # Update the node embedding with the neighbour messages.
        return self.update(node_repesentations, aggregated_messages)



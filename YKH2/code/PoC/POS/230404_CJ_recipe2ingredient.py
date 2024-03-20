# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:29:14 2023

@author: kyoo02
"""

import numpy as np
import pandas as pd
from itertools import chain
from tqdm import tqdm
from keras.utils import to_categorical

dt_root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code2/c_project/YKH/data/"
recipe  = dt_root + "CJ_recipe.csv"
diction = dt_root + "CJ_SKUDict.csv"
master  = dt_root + "CJ_master.csv"
noword  = dt_root + "CJ_noword.csv"

recipe_file = pd.read_csv(recipe, encoding="cp949")
dict_file   = pd.read_csv(diction)
master_file = pd.read_csv(master)
noword_file = pd.read_csv(noword)

menu_all = recipe_file["음식"]
dict_all = np.unique(dict_file["Dictionary_re"])

menu_name = []
for i in range(len(master_file.columns)):
    if master_file.columns[i].startswith("m_"):
        menu_name.append(master_file.columns[i][2:])

menu_in = []
for i in range(len(menu_name)):
    if menu_name[i] in set(menu_all):
        menu_in.append(0)
    else:
        menu_in.append(1)

menu_in_dt = pd.DataFrame({"menu":menu_name, "in":menu_in})


ingredient = []
for j in menu_name:
    #print(j)
    try:
        ing_unit = list(eval(list(recipe_file[recipe_file["음식"]==j]["재료"])[0]))
        ingredient.append(ing_unit)
    except:
        ingredient.append(j)
        continue

ing_new = list(chain(*ingredient))
ing_final = list(set(ing_new))

#pd.DataFrame(ing_final).to_csv("ing_final.csv",encoding="utf-8-sig")
word = np.setdiff1d(np.array(ing_final),np.array(noword_file["noword"]))


def jaccard_similarity(word_ref, word_list):
    s1 = set(word_ref)
    
    score = []
    for l in range(len(word_list)):
        s2 = set(word_list[l])
        score_unit = float(len(s1.intersection(s2)) / len(s1.union(s2)))
        score.append(score_unit)
    
    dt = pd.DataFrame({"Word" : word_list, "Score" : score})
    dt = dt.sort_values(by="Score", ascending=False)
    dt = dt.drop_duplicates()
    return dt


column_list = []

for i in tqdm(range(len(word)),desc = "Word Sim"):
    column_list.append(jaccard_similarity(word[i], dict_all)["Word"].iloc[0])

column_set = list(set(column_list))

ingre_master_data = pd.DataFrame(np.zeros([len(master_file),len(column_set)]),columns=column_set)

master_menu = master_file.filter(regex='^(m_).+',axis=1)


for l in tqdm(range(len(master_file)),desc="Deco Ingre"):
    loc = np.where(master_menu.iloc[l]>0)[0]
    menu_org = master_menu.columns[loc]
    menu_re = []
    for i in range(len(menu_org)):
        menu_re.append(menu_org[i][2:])
    
    ingre = [] 
    for t in menu_re:
        try:
            ing_unit = list(eval(list(recipe_file[recipe_file["음식"]==t]["재료"])[0]))
            ingre.append(ing_unit)
        except:
            ingre.append(j)
            continue
    
    ingre_new = list(chain(*ingre))
    ingre_final = list(set(ingre_new))
    ingre_final_noword = np.setdiff1d(np.array(ingre_final),np.array(noword_file["noword"]))

    ingre_list = []
    
    for i in range(len(ingre_final_noword)):
        ingre_list.append(jaccard_similarity(ingre_final_noword[i], dict_all)["Word"].iloc[0])
    
    ingre_set = list(set(ingre_list))
    
    for ii in range(len(ingre_set)):
        ingre_master_data.iloc[l][ingre_set[ii]]=1

cc = ingre_master_data.columns
cc_name = []
for c in range(len(cc)):
    cc_name.append("a_"+cc[c])

ingre_master_data.columns = cc_name

ingre_master_data.to_csv("ingred.csv",encoding="utf-8-sig")
    










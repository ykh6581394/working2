# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:07:50 2023

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
master_file = pd.read_csv(master, encoding="cp949")
noword_file = pd.read_csv(noword)

maindish = master_file["main"]

ingredient = []
for j in maindish:
    #print(j)
    if type(j)==str:
        ing_unit = list(eval(list(recipe_file[recipe_file["음식"]==j]["재료"])[0]))
        ing_unit2 = np.setdiff1d(np.array(ing_unit),np.array(noword_file["noword"]))
        ingredient.append(list(ing_unit2))
    else:
        ingredient.append([])

master_file["main_ingre"] = ingredient
master_file.to_csv("CJ_master.csv",index=False,encoding="utf-8-sig")









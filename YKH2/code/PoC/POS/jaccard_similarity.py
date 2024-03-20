# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 08:51:05 2023

@author: kyoo02
"""

import numpy as np
import pandas as pd
from Similiarity_API import *
from googletrans import Translator


"""
category = np.unique(df["상품범주(세)"])
dic_category = []
for c in range(len(category)):  
    df_sel = df[df["상품범주(세)"]==category[c]]["product"]
    sentence = mkSentence(df_sel)
    dic_category.append(sentence)
"""


def mkSentence(data):
    data = np.array(data)
    senten = []
    for j in range(len(data)):
        senten.append(data[j])
    return senten


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


def mkDt(root):

    df = pd.read_excel(root,
                     sheet_name = "Sheet1")
    dic_product = [] 
    for i in range(len(df)):
        row = df["상품명"].iloc[i].split("(")[0]
        try:
            row = row.replace("CK","")
        except:
            continue
        row = row.replace(" ","")
        dic_product.append(row)
    
    df["product"] = dic_product
    return df

def printResult(word_ref, top, df):
    sim_se   = jaccard_similarity(word_ref, df["상품범주(세)"])
    sim_pro  = jaccard_similarity(word_ref, df["상품명"])
    sim_dic1 = jaccard_similarity(word_ref, df["Dictionary"])
    sim_dic2 = jaccard_similarity(word_ref, df["Dictionary_re"])
    
    print("===========================")
    print(word_ref)
    print("===========================")
    print("\n상품범주")
    print(sim_se.head(top))
    print("\n상품명")
    print(sim_pro.head(top))
    print("\n1차 Cleansing")
    print(sim_dic1.head(top))
    print("\n2차(Human) Cleansing")
    print(sim_dic2.head(top))
    
    print("상품 리스트")
    
    dt_price = pd.DataFrame({"Product" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["상품명"],
                             "Price" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["매출금액(취급고기준)"]                    
                             })
    dt_price = dt_price.sort_values(by="Price", ascending=False)
    print(dt_price.head(10))

def dictIn(sim_dt, dictionary):
    
    names = sim_dt["name"]
    
    setin = []
    for s in range(len(names)):
        if names[s] in set(dictionary):
            setin.append("In")
        else:
            setin.append("N")
    sim_dt["set"] = setin
    return sim_dt
    
def trans(word_ref, translator):
    trans  = translator.translate(word_ref,src="ko",dest="en").text
    transs = translator.translate(trans,src="en",dest="ko").text
    return transs

if __name__ == "__main__":
    
    root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code2/c_project/YKH/data/CJFW/SKU_dict_final.xlsx"
    word_ref = "쉬림프"
    top      = 5
    close    = True
    similar  = False
    
    df = mkDt(root)
    printResult(word_ref, top, df)
    
    if close:
        try:
            print("==================== Close ========================")
            sim_word = naverDictCrawling(word_ref)   
            sim_word_n = dictIn(sim_word, df["Dictionary_re"])
            
            print(sim_word_n)
        
            word_ref_s = sim_word_n.iloc[0]["name"]
            printResult(word_ref_s, top, df)
        
        except:
            print("No close words")

        
    
    if similar:
        try:
            print("================= Similar Word ====================")
            sim_word = wordSim(word_ref, "ko")        
            sim_word_n = dictIn(sim_word, df["Dictionary_re"])
            sim_word_n = sim_word_n[sim_word_n["set"]=="In"]
            print(sim_word)
            print(sim_word_n)
            
            translator = Translator()
            trans(word_ref, translator)
            word_ref_t = trans(word_ref, translator)
            word_ref_s = sim_word_n.iloc[0]["name"]
            printResult(word_ref_s, top, df)
            print("================= Translator ====================")
            printResult(word_ref_t, top, df)
        except:
            print("No similar words")

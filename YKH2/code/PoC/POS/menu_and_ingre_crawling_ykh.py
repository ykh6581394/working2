# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:47:53 2023

@author: kyoo02
"""

import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


result = pd.DataFrame({'음식':[1],'재료':[1]})


for i in tqdm(range(9), desc="Nation Code"):
    nation_num = str(10*i+10)
    page_number=0
    
    tt = time.time()
    while True:
        
        
        #print(page_number)
        html = urlopen("https://www.menupan.com/Cook/recipere.asp?nation=" + nation_num +"&page="+str(page_number))
        bsObject = BeautifulSoup(html, "lxml", from_encoding='utf-8')
        
        #메뉴 수집
        menus = bsObject.findAll('span', {"class":"link"})
    
        menu_list = []
        for menu in menus:
            menu_tmp =menu.get_text()
            menu_list.append(menu_tmp)
        fd_nm = pd.DataFrame({'음식':menu_list})
        
      
        if len(fd_nm)==0:
            break
    
        # 재료 수집
        ingredients= bsObject.findAll('td', {"valign":"top"})
        ingred_list = []
    
        for ingredient in ingredients[5:]:
            tmp = ingredient.findAll('td')
            for i in tmp:
                tmp_text = i.get_text()
                if tmp_text ==None:
                    continue
                else:
                    if '주재료:' in tmp_text:
                        ingred_list.append(tmp_text[4:].split())
        ingred_nm = pd.DataFrame({'재료': ingred_list})
        
        tmp_result = pd.concat([fd_nm, ingred_nm],axis=1)
        
        result = pd.concat([result, tmp_result])
        page_number +=1
        
        print(time.time()-tt)

result = result[1:]
result = result.set_index(np.array(range(len(result))))

def find_key_zacard(A,B):
    #A는 입력 데이터
    #B는 컬럼
    tmp_similar=0
    key=""
    for i in B:
        #print(i)
        
        intersection_cardinality = len(set.intersection(*[set(A), set(i)]))
        union_cardinality = len(set.union(*[set(A), set(i)]))
        similar = intersection_cardinality / float(union_cardinality)
       
        
        if similar >= tmp_similar:
            key = i
            tmp_similar = similar
        #print(similar)
        #print(key)
          
    return key

def find_ingred(input_dt,result):
    found_key = find_key_zacard(input_dt,result['음식'])
    
    tmp_ingred_ = result[result['음식']==found_key]
    tmp_ingred_ = tmp_ingred_.set_index(np.array(range(len(tmp_ingred_))))
    final = []
    
    for i in range(len(tmp_ingred_)):
        final = final + tmp_ingred_['재료'][i]
        
    final = set(final)
    #print(found_key)
    
    return [found_key,final]


input_dt = "시저 샐러드"

find_ingred(input_dt, result)

ingredient = []

from itertools import chain

for i in range(len(result)):
    ingredient.append(result["재료"].iloc[i])

ing = list(chain(*ingredient))

ingredient2 = []

for i in range(len(ing)):
    if ing[i][-1] == ",":
        ingredient2.append(ing[i][:-1])
    else:
        ingredient2.append(ing[i])
    
ing_fin = list(set(ingredient2))





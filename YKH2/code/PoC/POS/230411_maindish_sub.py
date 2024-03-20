# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:09:13 2023

@author: kyoo02
"""

import numpy as np
import pandas as pd



root = 'C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code2/c_project/YKH/data/PoC/'
filename = "POS_데이터_20230327 (1).xlsx"

dt = pd.read_excel(root+filename,sheet_name='RESULT')

rs_list = np.unique(dt["STORE_NM"])

def menuUniq(r):
    print(rs_list[r])
    sel_dt = dt[dt["STORE_NM"]==rs_list[r]]
    a,b=np.unique(sel_dt["PRODUCT_NM"],return_counts=True)
    data = pd.DataFrame({"menu":a, "count":b})
    df = data.sort_values(by="count", ascending=False)
    
    print(df.head(10))

for i in range(len(rs_list)):
    try:
        menuUniq(i)
        print(" ")
    except:
        print('!!!!!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!!!!!!!')
        print(rs_list[i])
        print('!!!!!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!!!!!!!')    
        continue
    
    
    
menuUniq(59) 
    
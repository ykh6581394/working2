# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 08:58:16 2023

@author: kyoo02
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
from itertools import chain


root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Data/DynamicPricing/외식_상품별.csv"

data = pd.read_csv(root, encoding = "cp949")

category = []
for i in range(len(data)):
    dt_sel = data.iloc[i]
    unit = dt_sel["Category1"]+dt_sel["Category2"]+dt_sel["Category3"]+dt_sel["Category4"]
    category.append(unit)


category_uniq = np.unique(data["Category4"])

sum_all = []
for i in range(len(category_uniq)):
    dt_sel = data[data["Category4"]==category_uniq[i]]
    
    summary = []
    
    for j in range(len(dt_sel)):
        try:
            be1 = (int(dt_sel["매출1"].iloc[j].replace(",",""))-int(dt_sel["원가1"].iloc[j].replace(",",""))) #* int(dt_sel["SKU1"].iloc[j].split(" ")[0])
        except:
            be1 = 0
        try:
            be2 = (int(dt_sel["매출2"].iloc[j].replace(",",""))-int(dt_sel["원가2"].iloc[j].replace(",",""))) #* int(dt_sel["SKU2"].iloc[j].split(" ")[0])
        except:
            be2 = 0
        try:
            be3 = (int(dt_sel["매출3"].iloc[j].replace(",",""))-int(dt_sel["원가3"].iloc[j].replace(",",""))) #* int(dt_sel["SKU3"].iloc[j].split(" ")[0])
        except:
            be3 = 0
        
        summary.append([be1,be2,be3])
    
    
    aa=list(chain(*[list(np.sum(summary,axis=0)),[len(dt_sel)]]))
    sum_all.append(aa)
sum_all = np.array(sum_all)

sum_dt = pd.DataFrame({"Category" : category_uniq,
                       "Benefit1" : sum_all[:,0],
                       "Benefit2" : sum_all[:,1],
                       "Benefit3" : sum_all[:,2],
                       "Benefit"  : np.sum(sum_all[:,:3],axis=1),
                       "Unique"   : sum_all[:,3]
                       })

dt_sort = sum_dt.sort_values(by='Benefit' ,ascending=False)

sel = 10
plt.figure(figsize=(20,5),dpi=500)
plt.subplot(1,2,1)
plt.scatter(dt_sort["Category"][:sel],dt_sort["Benefit"][:sel])
plt.xticks(rotation=70)
plt.rc('font', size=20)  
plt.ylabel("영업이익(10억원)")
plt.grid(True,alpha=0.5, linestyle='--')

plt.subplot(1,2,2)
plt.scatter(dt_sort["Category"][:sel],dt_sort["Unique"][:sel],color="red")
plt.xticks(rotation=70)

plt.ylabel("상품 개수")
plt.grid(True,alpha=0.5, linestyle='--')
#plt.savefig("my.png",dpi=500)
plt.show()


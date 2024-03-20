# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 07:48:09 2023

@author: kyoo02
"""

import pandas as pd
import numpy as np
import plotly.express as px
from matplotlib import pyplot as plt




root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Data/식봄/"

dt = pd.read_excel(root+"주문조회_20230210_160219.xlsx",
                 sheet_name = 'Sheet1',)


sel_id = np.unique(dt["구매자 ID"])

budget = []
address = []
order_num = []
for i in range(len(sel_id)):
    
    dt_sel = dt[dt["구매자 ID"]==sel_id[i]]
    budget.append(sum(dt_sel["총 주문금액"]))
    address.append(dt_sel["배송지"].iloc[0])
    order_num.append(len(dt_sel))

dt_budget = pd.DataFrame({"user_id":sel_id, 
                          "budget":budget,
                          "address":address, 
                          "order":order_num
                          })

dt_sort = dt_budget.sort_values(by=["budget"],ascending=False)

plt.scatter(dt_sort["budget"],dt_sort["order"])
plt.hist(dt_sort["budget"])


sel_pro = np.unique(dt["상품명"])

budget = []
order_num = []
for i in range(len(sel_pro)):
    
    dt_sel = dt[dt["상품명"]==sel_pro[i]]
    budget.append(sum(dt_sel["총 주문금액"]))
    order_num.append(len(dt_sel))

dt_pro = pd.DataFrame({"pro_id":sel_pro, 
                          "budget":budget,
                          "order":order_num
                          })

dt_sort = dt_pro.sort_values(by=["budget"],ascending=False)
plt.hist(dt_sort["order"])












dt_mat = pd.DataFrame(np.zeros([len(np.unique(dt["배송지명"])),len(np.unique(dt["상품명"]))]),
    columns=np.unique(dt["상품명"]),
    index=np.unique(dt["배송지명"]))

for i in range(dt_mat.shape[0]):
    dt_sel = np.unique(dt[dt["배송지명"]==dt_mat.index[i]]["상품명"], return_counts=True)
    for j in range(len(dt_sel[0])):
        dt_mat[dt_sel[0][j]].loc[dt_mat.index[i]] = dt_sel[1][j]
    

dt_np = np.transpose(np.array(dt_mat))

from sklearn.manifold import TSNE
tsne_np = TSNE(n_components = 2).fit_transform(dt_np)














sel_id = np.unique(dt["구매자 ID"])
sel_pro = np.unique(dt["상품명"])

dt_sel = dt[dt["구매자 ID"]==sel_id[1]]["상품명"]

sel_uniq = np.unique(dt_sel,return_counts=True)
pd.DataFrame(np.transpose(sel_uniq[1]),columns=sel_uniq[0])



pro_in = []
for j in len(sel_pro):
    sel_uniq = np.unique(dt_sel,return_counts=True)
    if sel_pro[j] in sel_uniq[0]:
        pro_in.append(sel_uniq)


dt.pivot(index = dt["배송지명"], columns=dt["상품명"])



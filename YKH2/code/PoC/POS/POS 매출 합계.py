# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:54:14 2023

@author: kyoo02
"""

import pandas as pd
import numpy as np

root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code2/c_project/YKH/data/PoC/POS_230328.xlsx"

data = pd.read_excel(root, sheet_name ="RESULT")

name = data["상호명"]
name_uniq = np.unique(name)

ymd = []
ymd_col = []
for i in range(len(data["TRAN_YMDTIME"])):
    ymd.append(str(data["TRAN_YMDTIME"][i])[:8])
    ymd_col.append("d"+str(data["TRAN_YMDTIME"][i])[:8])

ymd_np = np.unique(ymd)
ymd_col = np.unique(ymd_col)

data["ymd"] = ymd





data_all = []
data_name = []

for i in range(len(name_uniq)):
    data_unit = []
    data_sel = data[data["상호명"]==name_uniq[i]]
    data_name.append(name_uniq[i])
    
    for j in range(len(ymd_np)):
        data_sales = data_sel[data_sel["ymd"]==ymd_np[j]]
        data_unit.append(np.sum(data_sales["TOTAL_SALES"]))
        
    data_all.append(data_unit)

sales_dt = pd.DataFrame(data_all,columns = ymd_col)
sales_dt["name"] = data_name
sales_dt.to_csv("sales_dt.csv",encoding="cp949")
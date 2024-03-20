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


root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code/c_project/YKH/data/CJFW/외식_상품별.csv"

data = pd.read_csv(root, encoding = "cp949")

category = []
for i in range(len(data)):
    dt_sel = data.iloc[i]
    unit = dt_sel["Category1"]+dt_sel["Category2"]+dt_sel["Category3"]+dt_sel["Category4"]
    category.append(unit)


category_uniq = np.unique(data["Category4"])

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:50:32 2023

@author: kyoo02
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/CJmaster.csv"

dt = pd.read_csv(root)


### FO, FW ###

dtc = dt[dt["category"]!="POS"]

plt.boxplot([dtc["buy12"].astype(int),
             dtc["buy1"].astype(int),
             dtc["buy1"].astype(int)],sym="r+")

plt.xticks([1, 2, 3],['22.12', '23.01', "23.02"])
plt.ylabel("10 Million Won")
plt.ylim([0,11000000])
plt.show()

### FO ###
dtc = dt[dt["category"]=="FO"]


dt12 = list(dtc["buy12"].astype(int))
dt12.sort()
dt12 = dt12[1:]
dt1 = list(dtc["buy1"].astype(int))
dt1.sort()
dt1 = dt1[1:]
dt2 = list(dtc["buy2"].astype(int))
dt2.sort()
dt2 = dt2[1:]

print("min 12 : {}".format(np.min(dt12)))
print("min 1 : {}".format(np.min(dt1)))
print("min 2 : {}".format(np.min(dt2)))
print("max 12 : {}".format(np.max(dt12)))
print("max 1 : {}".format(np.max(dt1)))
print("max 2 : {}".format(np.max(dt2)))
print("mean 12 : {}".format(np.mean(dt12)))
print("mean 1 : {}".format(np.mean(dt1)))
print("mean 2 : {}".format(np.mean(dt2)))
print("median 12 : {}".format(np.median(dt12)))
print("median 1 : {}".format(np.median(dt1)))
print("median 2 : {}".format(np.median(dt2)))

plt.title("FO")
plt.boxplot([dt12,
             dt1,
             dt2],sym="r+")

plt.xticks([1, 2, 3],['22.12', '23.01', "23.02"])
plt.ylabel("10 Million Won")
plt.ylim([0,11000000])
plt.show()

### FW ###

dtc = dt[dt["category"]!="POS"]
dtc = dtc[dtc["category"]!="FO"]

dt12 = list(dtc["buy12"].astype(int))
dt12.sort()
dt12 = dt12[1:]
dt1 = list(dtc["buy1"].astype(int))
dt1.sort()
dt1 = dt1[1:]
dt2 = list(dtc["buy2"].astype(int))
dt2.sort()
dt2 = dt2[1:]

print("min 12 : {}".format(np.min(dt12)))
print("min 1 : {}".format(np.min(dt1)))
print("min 2 : {}".format(np.min(dt2)))
print("max 12 : {}".format(np.max(dt12)))
print("max 1 : {}".format(np.max(dt1)))
print("max 2 : {}".format(np.max(dt2)))
print("mean 12 : {}".format(np.mean(dt12)))
print("mean 1 : {}".format(np.mean(dt1)))
print("mean 2 : {}".format(np.mean(dt2)))
print("median 12 : {}".format(np.median(dt12)))
print("median 1 : {}".format(np.median(dt1)))
print("median 2 : {}".format(np.median(dt2)))

plt.title("FW")
plt.boxplot([dt12,
             dt1,
             dt2],sym="r+")

plt.xticks([1, 2, 3],['22.12', '23.01', "23.02"])
plt.ylabel("10 Million Won")
plt.ylim([0,11000000])
plt.show()


############### Pos ############################


dtc = dt[dt["category"]!="FW"]
dtc = dtc[dtc["category"]!="FO"]

dt12 = list(dtc["sales12"].astype(int))
dt12.sort()
dt12 = dt12[2:]
dt12 = np.array(dt12)*3
dt1 = list(dtc["sales1"].astype(int))
dt1 = np.array(dt1)*3
dt2 = list(dtc["sales2"].astype(int))
dt2 = np.array(dt2)*3

plt.title("POS")
plt.boxplot([dt12,
             dt1,
             dt2],sym="bo")

plt.xticks([1, 2, 3],['22.12', '23.01', "23.02"])
plt.ylabel("100 Million Won")
#plt.ylim([0,11000000])
plt.show()

print("min 12 : {}".format(np.min(dt12)))
print("min 1 : {}".format(np.min(dt1)))
print("min 2 : {}".format(np.min(dt2)))
print("max 12 : {}".format(np.max(dt12)))
print("max 1 : {}".format(np.max(dt1)))
print("max 2 : {}".format(np.max(dt2)))
print("mean 12 : {}".format(np.mean(dt12)))
print("mean 1 : {}".format(np.mean(dt1)))
print("mean 2 : {}".format(np.mean(dt2)))
print("median 12 : {}".format(np.median(dt12)))
print("median 1 : {}".format(np.median(dt1)))
print("median 2 : {}".format(np.median(dt2)))






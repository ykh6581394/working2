# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:28:26 2023

@author: kyoo02
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim

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

def printResult(word_ref, top, df):
    #sim_se   = jaccard_similarity(word_ref, df["상품범주(세)"])
    #sim_pro  = jaccard_similarity(word_ref, df["상품명"])
    #sim_dic1 = jaccard_similarity(word_ref, df["Dictionary"])
    sim_dic2 = jaccard_similarity(word_ref, df["Dictionary_re"])

    dt_price = pd.DataFrame({"Product" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["상품명"],
                             "Price" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["매출금액(취급고기준)"]                    
                             })
    dt_price = dt_price.sort_values(by="Price", ascending=False)
    #print(dt_price.head(10))
    return sim_dic2.head(top), dt_price.head(top)




def ingreExt(ing_list):
    ing_par = []
    for ii in range(len(ing_list)):
        ing_par.append(ing_list[ii].split("_")[1])
    return ing_par


def addressLatong(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
   
    lat = geo.latitude
    lng = geo.longitude
    
    return lat, lng


def cjDataMaker(root, month, dt_name, dict_name, sim_mat, number):
    data = pd.read_csv(root + dt_name)
    diction = pd.read_csv(root + dict_name)
    simmat  = pd.read_csv(root + sim_mat, encoding="cp949")
    
    lat_a  = []
    long_a = []
    for l in tqdm(range(len(data)), desc="lat,long ext"):
        
        lat,long = addressLatong(data["address"][l])
        #print(data["address"][l])
        lat_a.append(lat)
        long_a.append(long)
    
    CJ_name = data["name"]
    CJ_addr = data["address"]
    CJ_cate = data["category"]
    
    sim_restaurant = []
    for n in range(len(CJ_name)):
        if CJ_name[n] in set(simmat[simmat.columns[0]]):
            loc = np.argmax(simmat.iloc[n][1:])
            sim_restaurant.append(simmat.columns[loc+1])
        elif CJ_name[n] in set(simmat.columns):
            restu = simmat[CJ_name[n]]
            loc = np.argmax(restu)
            sim_restaurant.append(simmat[simmat.columns[0]][loc])
            

    
    menu_all = data.filter(regex='^(a_).+',axis=1)
    menu_12  = data.filter(regex='^(b12_).+',axis=1)
    menu_1   = data.filter(regex='^(b1_).+',axis=1)
    menu_2   = data.filter(regex='^(b2_).+',axis=1)
    
    if month == 12:
        menu_month = menu_12
        buy_real   = data["buy12"]
        sale_real  = data["sales12"]
    elif month == 1:
        menu_month = menu_1
        buy_real   = data["buy1"]
        sale_real  = data["sales1"]
    elif month == 2:
        menu_month = menu_2
        buy_real   = data["buy2"]
        sale_real  = data["sales2"]
    
    ingre_all = []
    for i in range(menu_all.shape[0]):
        ingre_unit = []
        for j in range(menu_all.shape[1]):
            if menu_month.iloc[i][j]>0 and menu_all.iloc[i][j]>0:
                ingre_unit.append(menu_month.iloc[i][j])
            elif menu_month.iloc[i][j]==0 and menu_all.iloc[i][j]>0:
                ingre_unit.append(-1)
            else:
                ingre_unit.append(0)
        ingre_all.append(ingre_unit)
    
    ingre_all_pd = pd.DataFrame(ingre_all, columns = menu_all.columns)
    
    def sowBuy(loc):
    
        sow = ingre_all_pd.iloc[loc][ingre_all_pd.iloc[loc]==-1]
        buy = ingre_all_pd.iloc[loc][ingre_all_pd.iloc[loc]>0]
        all_l = ingre_all_pd.iloc[loc][ingre_all_pd.iloc[loc]!=0]
        all_list  = ingreExt(all_l.index)
        buy_list  = ingreExt(buy.index)
        buy_budge = list(buy)
        sow_list  = ingreExt(sow.index)
        if len(all_list)>0:
            buy_rate  = round(100*len(buy_list) / len(all_list),2)
        else:
            buy_rate = 0
        return [all_list, buy_rate, buy_list, buy_budge, sow_list]
    
        
    def salesSel(sow_list, number):
        sales_sel = []
        for k in range(len(sow_list)):
            soww = sow_list[k]
            #print(k)
            if len(soww)>0:
                sales_sel.append(list(np.random.choice(soww,number)))
            else:
                sales_sel.append([])
        return sales_sel
    
    wallet = []
    for b in range(len(buy_real)):
        buy_unit = buy_real[b]
        if buy_unit == "N":
            buy_unit = 0
        else:
            buy_unit = int(buy_unit)
        sales_unit = sale_real[b]
        if sales_unit == "small":
            sales_unit = 2100000
        elif sales_unit =="mid":
            sales_unit = 5000000
        elif sales_unit =="big":
            sales_unit = 15000000
        else:
            sales_unit = int(sales_unit)
        #wallet.append(round(100*buy_unit/(sales_unit+0.00001),2))
        wall = sales_unit-buy_unit
        if wall>0:
            wallet.append(wall)
        else:
            wallet.append(0)
    
    CJ_buy = []
    for j in range(len(ingre_all_pd)):
        CJ_buy.append(sowBuy(j))
    
    col_name = ["all_list","buy_rate","buy_list","buy_budget","sow_list"]
    CJ_dt = pd.DataFrame(CJ_buy, columns=col_name)
    CJ_dt["name"] = CJ_name
    CJ_dt["address"] = CJ_addr
    CJ_dt["category"] = CJ_cate
    CJ_dt["buy_real"] = buy_real
    CJ_dt["sales_real"] = sale_real
    CJ_dt["lat"] = lat_a
    CJ_dt["long"] = long_a
    CJ_dt["FCRS"] = data["FCRS"]
    CJ_dt["Sim"]  = sim_restaurant
    CJ_dt["wallet"] = wallet
    
    #sow_sel = salesSel(CJ_dt["sow_list"], number)
    #CJ_dt["recom"] = sow_sel
    main_reco = []
    ingredi_reco = []
    for re in range(len(CJ_dt)):
        sel = CJ_dt.iloc[re]
        if sel["category"] in set(["FO","FW"]):
            ingre_unit = data[data["name"]==sel["Sim"]]["main_ingre"]
            main_reco_unit = np.array(data[data["name"]==sel["Sim"]]["main"])[0]
            ingre_unit2 = eval(np.array(ingre_unit)[0])
            ingredi_reco.append(ingre_unit2)
            main_reco.append(main_reco_unit)
        elif sel["category"] in set(["POS","FWPOS"]):
            ingre_unit = CJ_dt[CJ_dt["name"]==sel["Sim"]]["buy_list"]
            ingre_unit2 = np.array(ingre_unit)[0]
            if len(ingre_unit2)==0:
                ingre_unit = data[data["name"]==sel["name"]]["main_ingre"]
                ingre_unit2 = eval(np.array(ingre_unit)[0])
            ingredi_reco.append(ingre_unit2)
            main_reco.append(data["main"][re])
    
    
    CJ_dt["Viz_ingredient_all"] = ingredi_reco
    sow_sel = salesSel(ingredi_reco, number)
    CJ_dt["Viz_ingredient_sel"] = sow_sel
    
    main_ingree = []
    
    for ttt in range(len(data["main_ingre"])):
        main_ingree.append(eval(data["main_ingre"][ttt]))
    
    CJ_dt["Viz_main_ingredient"] = main_ingree
    
    
    
    reco_product = []

    for s in tqdm(range(len(sow_sel)), desc="product matching"):
        product_unit = []
        sow_unit = sow_sel[s]
        for ss in range(len(sow_unit)):
            _, reco = printResult(sow_unit[ss], 5, diction)
            product_unit.append(list(reco["Product"]))
        reco_product.append(list(product_unit))

    main_reco_product = []

    for ss in tqdm(range(len(main_ingree)), desc="main product matching"):
        product_unit = []
        sow_unit = main_ingree[ss]
        for sss in range(len(sow_unit)):
            _, reco = printResult(sow_unit[sss], 3, diction)
            product_unit.append(list(reco["Product"]))
        main_reco_product.append(list(product_unit))

    CJ_dt["Viz_ingredient_product"] = reco_product
    CJ_dt["main"] = main_reco
    CJ_dt["main_product"] = main_reco_product
    
    return CJ_dt


if __name__ == "__main__":

    root = './Data/'

    month     = 12
    number    = 5
    dt_name   = "CJ_master.csv"
    dict_name = "CJ_SKUDict.csv"
    sim_mat   = "CJ_simmatrix.csv"

    
    result = cjDataMaker(root, month, dt_name, dict_name, sim_mat, number)
    result.to_csv(root+"CJ_m"+str(month)+".csv",encoding="utf-8-sig",index=False)
    

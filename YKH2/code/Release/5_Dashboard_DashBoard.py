# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:30:29 2023

@author: kyoo02
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main(root):
    @st.cache_data
    def dataLoader(root, filename):
        data = pd.read_csv(root + filename,encoding="utf-8-sig")
        return data
    
    st.sidebar.header("Select month")
    occupation = st.sidebar.selectbox("Select month",["22.12","23.01","23.02"])
    st.sidebar.write("You seleted ",occupation)
    
    if occupation == "22.12":
        filename = "CJ_m12.csv"
    elif occupation == "23.01":
        filename = "CJ_m1.csv"
    elif occupation == "23.02":
        filename = "CJ_m2.csv"
    master = "CJ_master.csv"
    
    img = Image.open(root + "CJ_log.png")
    
    
    st.image(img, width=310)
    st.title("CJ프레시웨이 외식 영업 추천")
    
    
    
    
    data_load_state = st.text('Loading data...')
    data = dataLoader(root, filename)
    master_dt = dataLoader(root, master)
    data_load_state.text("Data Loaded!")
    data_sel2 = data[['category','lat','long',
                     'name','buy_real','sales_real',"FCRS","Viz_ingredient_all",
                "address","main","wallet"
                ]]
    data_sel2.columns = ["category","위도","경도","매장명","CJ 판매액","월 매출","FC or RS","영업추천 식자재",
                        "주소","메인 메뉴","wallet"]
    
    cate = data_sel2["category"]
    mat = data_sel2["wallet"]
    buy_r = data_sel2["CJ 판매액"]
    mat_result = []
    for m in range(len(mat)):
        if cate[m] in set(["POS","FWPOS"]):
            mat_result.append(mat[m]*10/3)
        else:
            mat_result.append((mat[m]+int(buy_r[m]))*10/3)
    data_sel2["월 매출"] = mat_result
    
    st.subheader('마포구 영업지도')
    
    loc_map = st.container()
    
    with loc_map:
        st.text("마포구 기존/잠재 외식업체 분석 결과")
        
        walletsize = []
        for i in range(len(data_sel2["wallet"])):
            if data_sel2["wallet"][i]>0:
                walletsize.append(data["wallet"][i])
            else:
                walletsize.append(100000)
                
        category2 = []
        for i in range(len(data_sel2["category"])):
            if data_sel2["category"][i]=="FO":
                category2.append("기존고객(FO)")
            elif data_sel2["category"][i]=="FW":
                category2.append("기존고객(FW)")
            elif data_sel2["category"][i]=="FWPOS":
                category2.append("기존고객(FW)")
            elif data_sel2["category"][i]=="POS":
                category2.append("잠재고객")
        data["고객 분류"] = category2
        data["Wallet Size"] = walletsize
        data_sel2["고객 분류"] = category2
        data_sel2["Wallet Size"] = walletsize
        fig = px.scatter_mapbox(data_sel2, lat='위도', lon='경도', 
                                hover_name='매장명',                        
                                hover_data=["CJ 판매액","월 매출","FC or RS","영업추천 식자재",
                                            "주소","메인 메뉴" 
                                            ],
                                mapbox_style = "open-street-map",
                                color = "고객 분류",
                                size = "Wallet Size",
                                zoom=11) # open-street-map, carto_positron
        #fig.update_layout(mapbox={'style':"light",'zoom':7},showlegend=False)
        #fig.show()
        st.plotly_chart(fig)
    
    
    st.subheader('영업 추천 결과')
    st.text("기존 / 잠재 고객에 대한 영업 추천 결과")
    
    
    if st.checkbox("기존 고객 영업 추천"):
        data_sel = data[data["category"]!="POS"]
        data_sort = data_sel.sort_values("wallet",ascending=False)
        data_sort["SoW"] = data_sort["wallet"]
        data_sort["buy_real"] = data_sort["buy_real"].astype(int)
        data_show = data_sort[['name',
                               'address',
                               'main',
                               'SoW',                              
                               'buy_real',
                               'buy_list',
                               'Viz_ingredient_all',
                               'Viz_ingredient_product']]
        data_show.columns = ["매장명","주소","[추정]메인 메뉴","[추정]고객 잔여 Wallet",
                             "현재 판매 금액","판매 내역","[추천]판매 가능 식자재","[추천]판매 가능 상품"]
        data_show = data_show.reset_index(drop=True)
        st.write(data_show)
    if st.checkbox("잠재 고객 영업 추천"):
        data_sel = data[data["category"]=="POS"]
        data_sel["sales_real"] = round(10*(data_sel["sales_real"].astype(int))/3,0)
        data_sort = data_sel.sort_values("sales_real",ascending=False)
        M = max(data_sort["sales_real"])
        data_sort["new"] = round(100*(data_sort["sales_real"]/M),0)
        data_show = data_sort[["name",
                               "address",
                               "new",
                               "main",
                               "sales_real",
                               "Viz_main_ingredient",
                               "main_product",
                               'Viz_ingredient_all',
                               'Viz_ingredient_product']]
        data_show.columns = ["매장명",
                             "주소",
                             "잠재 영업 상대 가능성(%)",
                             "주력 메뉴",
                             "현재 매출(월)",           
                             "[추천]주력 메뉴 식자재",
                             "[추천]주력 메뉴 상품",
                             "[추천]유사 판매 가능 식자재","[추천]유사 판매 가능 상품"]
        data_show = data_show.reset_index(drop=True)
        st.write(data_show)      
                             
    
    if st.checkbox('Raw 데이터'):
        st.subheader('Raw data')
        st.write(data)
    
    
    
    st.subheader(" ")
    st.subheader('구매/매출 Trend(CJ거래 & POS정보 포함)')
    st.text("기존/잠재 고객의 구매, 매출 Trend(CJ거래 & POS정보 포함)")
    
    res = ["스푼필라프홍대점","인더썬", "테이커테이블"]
    sel1 = master_dt[master_dt["name"]==res[0]]
    sel2 = master_dt[master_dt["name"]==res[1]]
    sel3 = master_dt[master_dt["name"]==res[2]]
    master_dt_sel = pd.concat((sel1,sel2,sel3))
    ssales = master_dt_sel.filter(regex='^(d20).+',axis=1)
    sbuy   = master_dt_sel.filter(regex='^(sd20).+',axis=1)
    ssales.index = master_dt_sel["name"]
    sbuy.index = res
    
    
    date = []
    for i in range(len(ssales.columns)):
        date.append(ssales.columns[i].split("d")[1])
    
    sel_res = st.selectbox("외식업체 선택",
                       res)
    st.write(sel_res + " 는 CJ고객 & POS 정보가 있는 외식업체입니다.")
    
    time_dt = pd.DataFrame({"sales":list(ssales.loc[sel_res]), "buy":list(sbuy.loc[sel_res])})
    time_dt = time_dt.fillna(0)
    time_dt = time_dt.replace(',','', regex=True)
    time_dt = time_dt.astype(int)
    time_dt["date"] = pd.to_datetime(date)
    
    
    time_dt12 = time_dt[:31][["sales","buy"]].sum(axis=0)
    time_dt1  = time_dt[31:62][["sales","buy"]].sum(axis=0)
    time_dt2  = time_dt[62:][["sales","buy"]].sum(axis=0)
    time_dts = pd.concat((time_dt12,time_dt1,time_dt2),axis=1)
    time_dts = time_dts.transpose()
    time_dts["month"] = ["22년12월","23년01월","23년02"]
    
    data1 = go.Bar(x=time_dts["month"],y=time_dts["buy"], name="Purchese from CJ",
                   marker={"color":"rgba(208,191,228,1)"},width=0.34)
    data2 = go.Bar(x=time_dts["month"],y=time_dts["sales"], name="Sales to Customer",
                   marker={"color":"rgba(120,35,220,1)"},width=0.34)
    layout = go.Layout(title='월별 구매/매출 정보',
                       xaxis=dict(
                            title="Month"
                        ),
                        yaxis=dict(
                            title="KRW"
                        ) )
    fig4 = go.Figure(data=[data1, data2], layout=layout)
    st.plotly_chart(fig4)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=time_dt['date'], y=time_dt['sales'],
                              name="Sales to Customer",marker={"color":"rgba(120,35,220,0.8)"},
                              mode = 'lines+markers'
                              ))
    fig3.add_trace(go.Bar(x=time_dt['date'], y=time_dt['buy'],name="Purchese from CJ",
                          marker={"color":"rgba(208,191,228,1)"}))
    
    fig3.update_layout(height=600, width=800, title_text="Time Series Trend",
                       xaxis_title="Day",yaxis_title="KRW")
    
                      
    st.plotly_chart(fig3)
    
    
    
    
    ###############################################################################
    
    
    st.subheader(" ")
    st.subheader('구매/매출 Trend')
    st.text("기존/잠재 고객의 구매, 매출 Trend")
    res = master_dt["name"]
    ssales = master_dt.filter(regex='^(d20).+',axis=1)
    sbuy   = master_dt.filter(regex='^(sd20).+',axis=1)
    ssales.index = master_dt["name"]
    sbuy.index = res
    
                
    date = []
    for i in range(len(ssales.columns)):
        date.append(ssales.columns[i].split("d")[1])
    
    sel_res = st.selectbox("외식업체 선택",
                       res)
    st.write(sel_res + " 는 " +np.array(data[data["name"]==sel_res]["고객 분류"])[0] +" 입니다.")
    
    #sel_res = "미장플라쎄"
    
    time_dt = pd.DataFrame({"sales":list(ssales.loc[sel_res]), "buy":list(sbuy.loc[sel_res])})
    time_dt = time_dt.fillna(0)
    time_dt = time_dt.replace(',','', regex=True)
    time_dt = time_dt.astype(int)
    time_dt["date"] = pd.to_datetime(date)
    
    
    fig2 = make_subplots(rows=2, cols=1, subplot_titles=["Sales to Customer", "Purchase from CJ"],
                         x_title="Day",y_title="KRW",shared_xaxes=True,
                         vertical_spacing=0.1)
    
    fig2.append_trace(
        go.Bar(x=time_dt['date'], y=time_dt['sales'],name="Sales to Customer",
               marker={"color":"rgba(120,35,220,0.8)"}),row=1,col=1
        )
    fig2.append_trace(
        go.Bar(x=time_dt['date'], y=time_dt['buy'],name="Purchese from CJ",
               marker={"color":"rgba(208,191,228,1)"}),row=2,col=1
        )
    fig2.update_layout(height=600, width=800, title_text="Time Series Trend",
                       xaxis_title=" ",yaxis_title=" ")
    
                      
    st.plotly_chart(fig2)
    
    
if __name__ == "__main__":
    root ="./Data/"
    main(root)
    

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 07:44:30 2023

@author: kyoo02
"""

from tkinter import *
import numpy as np
import pandas as pd
from time import sleep
from googletrans import Translator
import openpyxl
import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

def trans(word_ref):
    translator = Translator()
    trans  = translator.translate(word_ref,src="ko",dest="en").text
    transs = translator.translate(trans,src="en",dest="ko").text
    return transs

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

    df = pd.read_csv(root)
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
    
    dt_price = pd.DataFrame({"Product" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["상품명"],
                             "Price" : df[df["Dictionary_re"]==sim_dic2.iloc[0]["Word"]]["매출금액(취급고기준)"]                    
                             })
    dt_price = dt_price.sort_values(by="Price", ascending=False)
    #print(dt_price.head(10))
    dt_price.to_csv("./1_Crawler_RecipeCrawler_SaveFile/CJ_sku_"+str(word_ref)+".csv",
                    index=False, encoding="utf-8-sig")
    sim_dic2.to_csv("./1_Crawler_RecipeCrawler_SaveFile/CJ_sim_"+str(word_ref)+".csv",
                    index=False, encoding="utf-8-sig")
    return sim_dic2.head(top), dt_price.head(5)

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

def naverDictCrawling(text, chr_root):
    
    url = 'https://ko.dict.naver.com/#/main'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = chr_root  # 크롬 설치 경로

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    
    #스파게티 입력하고 엔터
    search = driver.find_element(By.CSS_SELECTOR,'div.keyword_wrap > input.keyword')
    search.send_keys(text)  # 검색어 입력
    search.send_keys(Keys.ENTER)  # 엔터버튼 누르기
    
    sleep(3)
    link = driver.find_element(By.CSS_SELECTOR, 'div.option_area > div.sort_option > div > div > a:nth-child(4)')
    link.send_keys(Keys.ENTER)
    
    sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    buttons = soup.find_all('button',class_ = ['unit_add_wordbook', '_btn_add_wordbook'])
    
    similar_list= []
    for button in buttons:
        similar_list.append(button['entryname'])
    redt = pd.DataFrame({"name":similar_list})
    return redt


def simWord(word_ref, chr_root):
    sim_word = naverDictCrawling(word_ref, chr_root)   
    sim_word_n = dictIn(sim_word, df["Dictionary_re"])
    
    #print(sim_word_n)
    
    word_ref_s = sim_word_n.iloc[0]["name"]
    re = printResult(word_ref_s, top, df)
    return re[0], re[1]



def collect_menus(name, driver,result):
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 첫 메뉴 목록 찾기
    menu_lists = soup.select('.list_menu > li')
    menu_list=[]
    menu_detail_list=[]
    customer=[]
    
    for menu in menu_lists:
        
        menu_name = menu.select('.loss_word')[0].text
        menu_detail = menu.select('.txt_menu')# 리뷰
       
        
        menu_list.append(menu_name)
        menu_detail_list.append(menu_detail)
        customer.append(name)
        
    tmp_df = pd.DataFrame({'식당':customer,'메뉴이름':menu_list,'상세정보':menu_detail_list})

    return pd.concat([result, tmp_df])

def crawling_menus(loc, name, chr_root):
    #options = webdriver.ChromeOptions()
    
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = chr_root  # 크롬 설치 경로
    driver = webdriver.Chrome(options=chrome_options)  # chromedriver 열기
    
    
    driver.set_window_position(0, 0)
    driver.set_window_size(1000, 3000)
    driver.get('https://map.kakao.com/')
    
    result = pd.DataFrame({'식당':[1],'메뉴이름':[1],'상세정보':[1]})

    gu_name= loc
    rs_name = name
    
    name = gu_name +" " + rs_name
    
    driver.find_element(By.XPATH,'//*[@id="search.keyword.query"]').clear()
    
    search_area = driver.find_element(By.XPATH,'//*[@id="search.keyword.query"]')
    #검색 단어 
    search_area.send_keys(name)

    driver.find_element(By.XPATH,'//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
    
    time.sleep(3)


    #해당 음식점 창 열기
    search = driver.find_element(By.XPATH, '//*[@data-id="moreview"]')
    search.send_keys(Keys.ENTER)

    time.sleep(2)

    #열어진 창에서 작업
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(2) #

    #메뉴 가져오는 함수
    result = collect_menus(name, driver, result)

    driver.close()

    driver.switch_to.window(driver.window_handles[-1])

    return result[1:]




def zacard(A,B):
    intersection_cardinality = len(set.intersection(*[set(A), set(B)]))
    union_cardinality = len(set.union(*[set(A), set(B)]))
    similar = intersection_cardinality / float(union_cardinality)
    
    return similar

def find_ingred(menu_name,recipe):
    main_score=0
    main_menu=""
    
    for menu in recipe['음식']:
        tmp_score = zacard(menu, menu_name)
        
        if tmp_score > main_score:
            main_score = tmp_score
            main_menu = menu
    return main_menu

def matching_menu_ingred(crawled_menu, recipe):
    #레시피 불러오기
    #adr=""
    #recipe = pd.read_csv('C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code/c_project/c_project/YKH/data/통합레시피_유니크.csv',encoding = 'euc-kr')
    ingred_list =[]

    for i in range(len(crawled_menu)):
    
        tmp1 = find_ingred(crawled_menu['메뉴이름'][i],recipe)
        

        ingred_list.append(recipe[recipe['음식']==tmp1]['재료'].item())

    ingred_list=pd.DataFrame({'재료':ingred_list})
    crawled_menu['재료'] = ingred_list

    return crawled_menu

def crawling_and_matching(loc, name, recipe, chr_root):
    crawled = crawling_menus(loc, name, chr_root)
    
    result = matching_menu_ingred(crawled, recipe)
    result.to_csv("./1_Crawler_RecipeCrawler_SaveFile/menu_"+name+".csv",
                    index=False, encoding="utf-8-sig")
    
    return result


if __name__ == "__main__":
    root = "./Data/CJ_SKUDict.csv"
    word_ref = "장아찌"
    top      = 5
    close    = True
    similar  = False
    mode     = "Crawler" # Crawler, Matcher
    chr_root = "C:/Users/kyoo02/AppData/Local/Google/Chrome/Application/chrome.exe"
    
    df = mkDt(root)
    recipe = pd.read_csv('./Data/CJ_recipe.csv',encoding='euc-kr')
    """
    loc = "서울 동작구 성대로 24"
    name = "여기로"
    menu_and_ingred = crawling_and_matching(loc, name, recipe).iloc[0]["재료"]
    """
    if mode == "Crawler":
        root2 = Tk()
        root2.title("Menu Crawler")
        root2.geometry("640x400+100+100")
        entry1 = Entry(root2, width=50, border=1, borderwidth=10)
        entry1.pack()
        entry2 = Entry(root2, width=50, border=1, borderwidth=10)
        entry2.pack()
        
        def btn0command():
            label = Label(root2, text=crawling_and_matching(entry1.get(), entry2.get(), recipe, chr_root)["메뉴이름"])
            label.pack()
        def btncommand():
            label = Label(root2, text=crawling_and_matching(entry1.get(), entry2.get(), recipe, chr_root)["재료"])
            label.pack()
            
        btn0 = Button(root2, text = "Print Menu", padx=20, pady=2, fg = "black", command = btn0command)
        btn0.pack(side = "left",anchor="n")
        btn = Button(root2, text = "Print Ingredient", padx=20, pady=2, fg = "black", command = btncommand)
        btn.pack(side = "left",anchor="n")
        root2.mainloop()
    
        
    elif mode == "Matcher": 
        root = Tk()
        root.title("Word Matcher")
        root.geometry("640x400+100+100")
        entry1 = Entry(root, width=50, border=1, borderwidth=10)
        entry1.pack()
        
        def btn1command():
            label1 = Label(root, text=printResult(entry1.get(), top, df)[0])
            label1.pack(side = "left",anchor = 'n')
        def btn2command():
            label2 = Label(root, text=printResult(entry1.get(), top, df)[1])
            label2.pack(side = "left",anchor = 'n')
        def btn3command():
            label3 = Label(root, text=simWord(entry1.get(),chr_root)[0])
            label3.pack(side = "top",anchor = 'n')
        def btn4command():
            label4 = Label(root, text=simWord(entry1.get(),chr_root)[1])
            label4.pack(side = "top",anchor = 'n')
        def btn5command():
            #print(trans(entry1.get()))
            label5 = Label(root, text=printResult(trans(entry1.get()), top, df)[0])
            label5.pack(side = "top",anchor = 'n')
        def btn6command():
            label6 = Label(root, text=printResult(trans(entry1.get()), top, df)[1])
            label6.pack(side = "top",anchor = 'n')
        def btn7command():
            label7 = Label(root, text=trans(entry1.get()))
            label7.pack(side = "top",anchor = 'n')
        
        btn1 = Button(root, text = "Dic 검색", padx=20, pady=1, fg = "black", command = btn1command)
        btn1.pack(side = "top",anchor="w")
        btn2 = Button(root, text = "Product", padx=20, pady=1, fg = "black", command = btn2command)
        btn2.pack(side = "top",anchor="w")
        btn3 = Button(root, text = "네이버 국어사전", padx=20, pady=1, fg = "black", command = btn3command)
        btn3.pack(side = "top",anchor="w")
        btn4 = Button(root, text = "유사 Product", padx=20, pady=1, fg = "black", command = btn4command)
        btn4.pack(side = "top",anchor="w")
        btn5 = Button(root, text = "번역상품", padx=20, pady=1, fg = "black", command = btn5command)
        btn5.pack(side = "top",anchor="w")
        btn6 = Button(root, text = "유사 Product", padx=20, pady=1, fg = "black", command = btn6command)
        btn6.pack(side = "top",anchor="w")
        btn7 = Button(root, text = "번역", padx=20, pady=1, fg = "black", command = btn7command)
        btn7.pack(side = "right",anchor="s")
        
        root.mainloop()


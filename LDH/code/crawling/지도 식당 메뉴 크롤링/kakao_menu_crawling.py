#!/usr/bin/env python
# coding: utf-8

# # 크롤링 코드

# In[1]:


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

def crawling_menus(df):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    #options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36   ")
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=options)  # chromedriver 열기
    driver.set_window_position(0, 0)
    driver.set_window_size(1000, 3000)
    driver.get('https://map.kakao.com/')
    
    result = pd.DataFrame({'식당':[1],'메뉴이름':[1],'상세정보':[1]})
    
    for i in range(len(df)):
        gu_name= df['지역'][i]
        rs_name = df['식당이름'][i]
        
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


# ## 레시피랑 매칭 작업

# In[9]:


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
    adr=""
    recipe = pd.read_csv(adr+'통합레시피_유니크.csv',encoding = 'euc-kr')
    ingred_list =[]

    for i in range(len(crawled_menu)):
    
        tmp1 = find_ingred(crawled_menu['메뉴이름'][i],recipe)
        

        ingred_list.append(recipe[recipe['음식']==tmp1]['재료'].item())

    ingred_list=pd.DataFrame({'재료':ingred_list})
    crawled_menu['재료'] = ingred_list
    return crawled_menu

def crawling_and_matching(df, recipe):
    crawled = crawling_menus(df)
    
    result =matching_menu_ingred(crawled, recipe)
    
    return result


# # 예시

# In[10]:


#예시 데이터
df= pd.DataFrame({'지역': ["서울 동작구 성대로 24"],'식당이름':["여기로"]})
recipe = pd.read_csv('통합레시피_유니크.csv',encoding='euc-kr')

#crawled_menu = crawling_menus(df)
#matching_menu_ingred(crawled_menu, recipe)

menu_and_ingred = crawling_and_matching(df, recipe)
menu_and_ingred


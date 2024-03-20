#!/usr/bin/env python
# coding: utf-8

# # New naver crawling code

# In[123]:



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
from selenium.webdriver.common.action_chains import ActionChains


def naver_map_crawling(address, name):
    url = 'https://map.naver.com/v5/search'
    driver = webdriver.Chrome()  # 드라이버 경로
    # driver = webdriver.Chrome('./chromedriver',chrome_options=options) # 크롬창 숨기기
    driver.get(url)
    
    time.sleep(12)
    
    search = driver.find_element(By.CSS_SELECTOR,'div.input_box > input.input_search')
    search.send_keys(address)  # 검색어 입력
    search.send_keys(Keys.ENTER)
    
    time.sleep(3)
    search = driver.find_element(By.CSS_SELECTOR,'div.input_box > input.input_search')
    search.send_keys(" "+name)  # 검색어 입력
    search.send_keys(Keys.ENTER)
    time.sleep(5)

    #바로 나오는 경우  ex 서울 동대문구 경희대로6길 3-2 에잇올리
    try:
        driver.switch_to.frame("entryIframe")
 
    
    except:

        #바로 안나오는경우 ex) 여기로
        driver.switch_to.frame("searchIframe")
        #첫번째 목록 클릭
        time.sleep(2)
        find_store_click = driver.find_element(By.CSS_SELECTOR,"#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.qbGlu > div.ouxiq.icT4K > a:nth-child(1)")
        find_store_click.click()
    

        time.sleep(2)
        driver.switch_to.default_content()
        driver.switch_to.frame("entryIframe")
    #메뉴 클릭
    find_menu_click = driver.find_element(By.XPATH, "//span[text()='메뉴']/parent::a")
    find_menu_click.click()

    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    menu_list = []

    menus = soup.find_all('div',class_ = 'tit')
    for menu in menus:
        menu_list.append(menu.text)
    
    menus = soup.find_all('span',class_ = 'Sqg65')
    for menu in menus:
        menu_list.append(menu.text)
    
    return menu_list
    


# In[120]:


adress = "서울 마포구 월드컵북로6길 12-13"  # 검색어
name= "다운타우너"

naver_map_crawling(adress, name)


# In[ ]:





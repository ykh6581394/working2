#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import re
import json


# In[8]:


def naver_dict_crawling(text):
    
    url = 'https://ko.dict.naver.com/#/main'
    driver = webdriver.Chrome() 
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
        
    return similar_list


# In[9]:


text = '스파게티'
sim_words = naver_dict_crawling(text)
sim_words


# In[ ]:





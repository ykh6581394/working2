import requests
import pandas as pd

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


def naverDictCrawling(text):
    
    url = 'https://ko.dict.naver.com/#/main'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "C:/Users/kyoo02/AppData/Local/Google/Chrome/Application/chrome.exe"  # 크롬 설치 경로

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



def wordSim(word, lang):
    url = "https://word-similarity2.p.rapidapi.com/api/v1/similar-words"
    
    payload = {
    	"word": word,
    	"lang": lang,
    	"wordnum": 10
    }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": "49c82b0456mshd287c7187278a80p1f4845jsn75ddc8944209",
    	"X-RapidAPI-Host": "word-similarity2.p.rapidapi.com"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    
    #print(response.text)
    result = eval(response.text)
    
    name = []
    value = []
    for i in range(len(result)):
        name.append(result[i]["name"])
        value.append(result[i]["value"])
    result_dt = pd.DataFrame({"name" : name, "value" : value})
    return result_dt
    

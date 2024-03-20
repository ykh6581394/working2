#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import numpy as np


# In[ ]:


df= pd.read_excel("C:/Users/KEARNEY/Desktop/새 폴더/c_project/YKH/data/PoC/POS_230328.xlsx",sheet_name='RESULT')


# In[7]:


df.head()


# In[9]:


df.columns


# In[13]:


df[df['TOTAL_AMT'] != df['TOTAL_SALES']]


# In[ ]:





# # 매장별 월별 매출 계산하고 top5메뉴 정리한 데이터 정리 
# 
# ## 예시
# 
# ### 매장1 | 주소 | 12월 매출액 | 1월 매출액 | 2월 매출액 | 12월 top5 |1월 top5 | 2월 top5 | 메뉴로 유추한 필요 식재료

# In[24]:


# 상호명 ADDR_K, TRAN_YMD, PRODUCT_NM,TOTAL_AMT
tmp_df = df[['상호명','ADDR_K','TRAN_YMD','PRODUCT_NM','TOTAL_AMT','YEAR','END_MONTH']]


# In[26]:


tmp_df.head()


# In[27]:


tmp_df.columns = ['상호명','주소','날짜','메뉴','매출','연','월']


# In[38]:


# 전체 상호명
total_store = tmp_df['상호명'].unique()
# column들
column_nm = ['주소','12월 매출액','1월 매출액','2월 매출액','전체 매출액','12월 top5','1월 top5','2월 top5']


# In[41]:


result_df = pd.DataFrame(index= total_store, columns=column_nm ).reset_index()


# In[80]:


result_df.columns = ['상호명', '주소', '12월 매출액', '1월 매출액', '2월 매출액', '전체 매출액', '12월 top5',
       '1월 top5', '2월 top5']
result_df['주소'] = df['ADDR_K'].unique()


# In[81]:


result_df.head()


# In[31]:


month_12_df = tmp_df[tmp_df['월']==12]
month_1_df = tmp_df[tmp_df['월']==1]
month_2_df = tmp_df[tmp_df['월']==2]

month_12_df = month_12_df.set_index(np.array(range(len(month_12_df))))
month_1_df = month_1_df.set_index(np.array(range(len(month_1_df))))
month_2_df = month_2_df.set_index(np.array(range(len(month_2_df))))


# In[49]:


month_12_df.head()


# In[72]:


# 매출부터 
sell_12 = month_12_df.groupby('상호명')['매출'].sum()
sell_1 = month_1_df.groupby('상호명')['매출'].sum()
sell_2 = month_2_df.groupby('상호명')['매출'].sum()

for i in sell_12.index:
    result_df.loc[result_df['상호명']==i, '12월 매출액'] = sell_12[i]
    
for i in sell_1.index:
    result_df.loc[result_df['상호명']==i, '1월 매출액'] = sell_1[i]
    
for i in sell_2.index:
    result_df.loc[result_df['상호명']==i, '2월 매출액'] = sell_2[i]
    
result_df['전체 매출액'] = result_df['12월 매출액']+result_df['1월 매출액']+result_df['2월 매출액']

result_df.head()


# In[101]:


#메뉴 빈도 조사
#top5 기준 매출액 기준


# In[179]:


result_df.head()


# In[183]:


sales_12 = month_12_df.groupby(['상호명','메뉴']).sum()

# 식당별 매출이 높은 상위 3개의 메뉴 선택
sales_12_top5 = sales_12.groupby('상호명').apply(lambda x: x.nlargest(5, '매출'))


sales_12_top5.index.names = ['상호명','상호명1','메뉴']

sales_12_top5 = sales_12_top5.reset_index()

top_5_12_df = sales_12_top5.groupby('상호명')['메뉴'].apply(list).reset_index(name='top 5 메뉴')

for i in top_5_12_df['상호명']:
    top5= top_5_12_df.loc[top_5_12_df['상호명']==i,'top 5 메뉴']
    result_df.loc[result_df['상호명']==i, '12월 top5'] = np.array(top5)

###########################################################################

sales_1 = month_1_df.groupby(['상호명','메뉴']).sum()

# 식당별 매출이 높은 상위 3개의 메뉴 선택
sales_1_top5 = sales_1.groupby('상호명').apply(lambda x: x.nlargest(5, '매출'))


sales_1_top5.index.names = ['상호명','상호명1','메뉴']

sales_1_top5 = sales_1_top5.reset_index()

top_5_1_df = sales_1_top5.groupby('상호명')['메뉴'].apply(list).reset_index(name='top 5 메뉴')

for i in top_5_1_df['상호명']:
    top5= top_5_1_df.loc[top_5_1_df['상호명']==i,'top 5 메뉴']
    result_df.loc[result_df['상호명']==i, '1월 top5'] = np.array(top5)
    
###########################################################################

sales_2 = month_2_df.groupby(['상호명','메뉴']).sum()

# 식당별 매출이 높은 상위 3개의 메뉴 선택
sales_2_top5 = sales_2.groupby('상호명').apply(lambda x: x.nlargest(5, '매출'))


sales_2_top5.index.names = ['상호명','상호명1','메뉴']

sales_2_top5 = sales_2_top5.reset_index()

top_5_2_df = sales_2_top5.groupby('상호명')['메뉴'].apply(list).reset_index(name='top 5 메뉴')

for i in top_5_2_df['상호명']:
    top5= top_5_2_df.loc[top_5_2_df['상호명']==i,'top 5 메뉴']
    result_df.loc[result_df['상호명']==i, '2월 top5'] = np.array(top5)
    


# In[184]:


result_df.head()


# In[220]:


result_df['사이즈'] = 10


# # 시각화

# In[221]:


#주소 -> 위도 경도 변환
from geopy.geocoders import Nominatim
import pandas as pd
import plotly.express as px

def address_lat(address):

    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    idx = address.find('(')
    
    address = address[:idx-1]
    
    geo = geolocoder.geocode(address)
    #crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
    
    lat = geo.latitude
    
    return lat

def address_lng(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    idx = address.find('(')
    
    address = address[:idx-1]
    
    geo = geolocoder.geocode(address)
    #crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
    
    lng = geo.longitude
    

    return lng

#그림 그리기
def plotly_ploting(df):
    

    lat =df['주소'].apply(address_lat)
    lng =df['주소'].apply(address_lng)

    df['lat']=lat
    df['lng']=lng
    
    fig = px.scatter_mapbox(df, lat='lat', lon='lng', hover_name='상호명',
                            hover_data=['12월 매출액','1월 매출액','2월 매출액','12월 top5','1월 top5','2월 top5'],
                           size='사이즈')
    fig.update_layout(mapbox_style = "open-street-map")
    fig.show()
    
def make_plot_complete(df):
    
    ploted_map = plotly_ploting(df)
    
    return ploted_map


# In[222]:


import re

def extract_address(text):
    pattern = re.compile(r'서울시\s마포구\s\w+\s\d+(-\d+)?')
    match = pattern.search(text)
    if match:
        return match.group()


# In[223]:


result_df['주소'] = result_df['주소'].apply(extract_address)


# In[224]:


map1 = make_plot_complete(result_df)


# In[ ]:


import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls
 
username = 'LDH_KN'
api_key = 'Lh1bR4Bj4yHVLeMZ7tzk'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
 
https://zephyrus1111.tistory.com/154


# In[234]:


result_df.head()


# In[ ]:





# In[ ]:





# # 시각화
# ### 매출 그래프

# In[237]:


bar_12_df = result_df.sort_values('12월 매출액', ascending=False)
px.bar(bar_12_df, x='상호명', y="12월 매출액")


# In[238]:


bar_1_df = result_df.sort_values('1월 매출액', ascending=False)
px.bar(bar_1_df, x='상호명', y="1월 매출액")


# In[239]:


bar_2_df = result_df.sort_values('2월 매출액', ascending=False)
px.bar(bar_2_df, x='상호명', y="2월 매출액")


# # 건수 그래프

# In[245]:


result_df['12월 거래량']= 0
result_df['1월 거래량']= 0
result_df['2월 거래량']= 0

count_12 = month_12_df.groupby('상호명').count()['주소']
count_1 = month_1_df.groupby('상호명').count()['주소']
count_2 = month_2_df.groupby('상호명').count()['주소']

for i in count_12.index:
    result_df.loc[result_df['상호명']==i, '12월 거래량'] = count_12[i]
    
for i in count_1.index:
    result_df.loc[result_df['상호명']==i, '1월 거래량'] = count_1[i]

for i in count_2.index:
    result_df.loc[result_df['상호명']==i, '2월 거래량'] = count_2[i]


# In[250]:


bar_12_df = result_df.sort_values('12월 매출액', ascending=False)
px.bar(bar_12_df, x='상호명', y="12월 매출액")


# In[251]:


bar_1_df = result_df.sort_values('1월 매출액', ascending=False)
px.bar(bar_1_df, x='상호명', y="1월 매출액")


# In[252]:


bar_2_df = result_df.sort_values('2월 매출액', ascending=False)
px.bar(bar_2_df, x='상호명', y="2월 매출액")


# In[ ]:





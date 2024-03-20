#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import joblib


def preprocess(data_root, data_name,category):
    
    df= pd.read_csv(data_root+data_name)
    
    # 원핫 인코딩을 위한 변환
    df['review1stComment'] = df['review1stComment']+"1"
    df['review2ndComment'] = df['review2ndComment']+"2"
    
    #sales 12부터 follow까지
    start_idx = df.columns.get_loc('sales12')
    end_idx = df.columns.get_loc('follow')+1
    
    #시작 인덱스
    #row_start_idx = df[df['category']=='POS'].index[0]
    
    #사용할 부분만 정리
    if category =="POS":
        tmp_df = df.iloc[df[(df['category']!='FW')&(df['category']!='FO')].index , start_idx:end_idx]
    elif category == "CJ":
        tmp_df = df.iloc[df[(df['category']=='FW')|(df['category']=='FO')].index , start_idx:end_idx]
    elif category=="TOTAL":
        tmp_df = df.iloc[:,start_idx: end_idx]
    
    #매장명 붙이기
    tmp_df['매장'] = df.iloc[:,0]
    
    #vistorrevie 없는것들 삭제(폐업)
    tmp_df = tmp_df.dropna(subset=["visitorReview"])
    
    #정수형 변환
    if category =="POS":
        tmp_df[['sales12','sales1','sales2']] = tmp_df[['sales12','sales1','sales2']].astype(float)
        #평균 매출
        tmp_df['total_sales'] = (tmp_df['sales12']+tmp_df['sales1']+tmp_df['sales2'])/3
    
    
    #2달치만 있는 것들 보정
    #sales12가 0인 인덱스들
    
        for idx in tmp_df[tmp_df['sales12'] ==0].index:
            tmp_df.loc[idx,'total_sales'] = tmp_df.loc[idx,'total_sales']*3/2
    
        #매출 10/3 곱함
        tmp_df['total_sales'] = tmp_df['total_sales']*10/3
    
        

        # 0.31, 0.75 기준으로 라벨링
        tmp_df['label'] = pd.cut(tmp_df['total_sales'], bins=[-float('inf'), 1*10**7, 3*10**7, float('inf')], labels=['small', 'mid', 'big'])
     
        #슬로우바비큐 삭제(최근에 생긴 가게로 급격히 매출 증가)
    tmp_df = tmp_df[tmp_df['매장'] != '슬로우야드 바비큐']   
        # 인스타 여부 변수로 추가
    tmp_df['instagram'] = np.where(tmp_df['follow'].isnull(), 0, 1)
    #tmp_df['label'].value_counts()
        
    return df, tmp_df



def one_hot_encode(df, columns):
    
    df= df.rename(columns={'매장':'식당'})
    
    one_hot_cols = set()
    
    for col in columns:
        tmp = pd.get_dummies(df[col])
        one_hot_cols = set(one_hot_cols) | set(tmp.columns)
        df = pd.concat([df,tmp], axis=1)
        
    return df, one_hot_cols

def rf_modeling(X,y):
    

    param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
    rf = RandomForestClassifier()
    
    cv = StratifiedKFold(n_splits=5)
    grid_search = GridSearchCV(rf, param_grid, cv=cv)
    
    grid_search.fit(X, y)
    
    print(grid_search.best_score_)
    
    # grid_search.best_params_ 이걸로 학습
    model = RandomForestClassifier(n_estimators= grid_search.best_params_['n_estimators'],
                                  max_depth = grid_search.best_params_['max_depth'],
                                  min_samples_split=grid_search.best_params_['min_samples_split'],
                                  min_samples_leaf=grid_search.best_params_['min_samples_leaf'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=999)
    
    model.fit(X_train, y_train)
    
    return model
    

    
def inference(root,dt_name,model,category):
    
    
    df , tmp_df = preprocess(root, dt_name,category)


    #tt 순서 맞춰주기
    tmp_df1, one_hot_var = one_hot_encode(tmp_df, ['review1stComment','review2ndComment'])
    
    X_var=['재료2','음식1','매장1','가성비1','혼밥2','서비스1','서비스2','가성비2',
     'review1st','instagram','양2','음악1','review2nd','술2','visitorReview',
     '인테리어2','인테리어1','뷰1','blogReview','메뉴2','음식2']
    
    #원핫 인코딩에없는것들 columns으로 추가
    add_columns = list(set(X_var)-set(tmp_df1.columns))
    
    for col in add_columns:
        tmp_df1[col] = 0
        
    tmp_df1= tmp_df1.loc[:,X_var]
    
    prediction = model.predict(tmp_df1[X_var])
    
  

    pred = pd.DataFrame({'식당': tmp_df['매장'] ,'wallet_size':prediction})

    
    return pred
    
    
    
def train(data_root, data_name):
    
    #데이터 전처리(데이터 자르고 target 설정 등)
    ##OK
    df, tmp_df = preprocess(data_root, data_name,"POS")
    
    #원핫 인코딩
    tmp_df, one_hot_var = one_hot_encode(tmp_df, ['review1stComment','review2ndComment'])
    
    
    #변수 정리
    basic_var = set(['visitorReview','blogReview', 'review1st','review2nd', 'instagram'])
    #one_hot_var = set(one_hot_encoded1.columns) | set(one_hot_encoded2.columns)
    X_var = list(basic_var | one_hot_var)
  
    
    X=tmp_df[X_var]
    y=tmp_df['label']
    
    
    model = rf_modeling(X,y)
    
    #infer = inference(df, model,X_var)
    
    return model



if __name__ == "__main__":
    data_root = 'C:/Users/KEARNEY/Desktop/새 폴더/c_project/LDH/release/data/'
    data_name = "CJ_master.csv"
    
    
    ###options
    mode="infer"  ## train, infer
    
    ##training options
    save_option = "save"  # save, no
    
    
    ##inference options
    category = "CJ"  # 'POS','CJ',"TOTAL"
    model_option = "load" # load, training
    
    
    
    if mode =="train":
        
        model = train(data_root,data_name)
        
        if save_option == "save":
            joblib.dump(model, 'C:/Users/KEARNEY/Desktop/새 폴더/c_project/LDH/release/wallet_prediction_model.pkl')
        
            
    elif mode == 'infer':
        
    
        if model_option == "load":
            model = joblib.load('C:/Users/KEARNEY/Desktop/새 폴더/c_project/LDH/release/wallet_prediction_model.pkl')
        
        infer = inference(data_root,data_name,model, category)
        

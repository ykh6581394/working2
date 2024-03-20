
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def prepro(df):
    #메뉴
    start_idx = df.columns.get_loc('m_치즈감자전')
    end_idx = df.columns.get_loc('m_버섯베이컨알프레도파스타')

    menu= df.iloc[:,start_idx:end_idx]
    
    # 식자재 a_혼합야채 to a_버팔로윙
    ing_start_idx = df.columns.get_loc('a_혼합야채')
    ing_end_idx = df.columns.get_loc('a_버팔로윙')
    
    ingred = df.iloc[:,ing_start_idx:ing_end_idx]
    
    # 리뷰등 공통 칼럼
    # "review1stComment",, "review2ndComment" 제외함 
    more_info = df[["visitorReview","blogReview","review1st", "review2nd","review1stComment", "review2ndComment" ]]

    
    #식당이랑 카테고리 칼럼 추가하고 순서 변경
    df1 = pd.concat([menu,ingred, more_info],axis=1)
    
    scaler = MinMaxScaler()

    # 칼럼 standardized
    df1[["visitorReview","blogReview","review1st", "review2nd"]] = scaler.fit_transform(df1[["visitorReview","blogReview","review1st", "review2nd"]])

    
    df1['category'] = df['category']
    df1 = df1[['category']+ df1.columns[:-1].to_list()]
    
    df1['식당']= df['name']
    df1 = df1[['식당']+ df1.columns[:-1].to_list()]
    
    df1 = pd.get_dummies(df1, columns=['review1stComment', 'review2ndComment'])
    
    #폐업 제거
    df1 = df1.dropna()
        
    return df1

def make_mat(df):
    #pos와 아닌것 분리해서 가져오기
    group_non_pos = df[(df['category'] == 'FW') | (df['category'] =='FO')].iloc[:, 2:].reset_index(drop=True)
    group_pos = df[(df['category'] == 'POS') | (df['category']=='FWPOS')].iloc[:, 2:].reset_index(drop=True)

    #인덱스 설정
    non_pos_idx= df[(df['category'] == 'FW') | (df['category'] =='FO')]['식당']
    pos_idx= df[(df['category'] == 'POS') | (df['category']=='FWPOS')]['식당']
    non_pos_idx.name= 'non pos 식당'
    pos_idx.name= 'pos 식당'
    
    #유사도 행렬 만들기
    similarity_matrix = cosine_similarity(group_non_pos, group_pos)
    similarity_df = pd.DataFrame(similarity_matrix, index=non_pos_idx, columns=pos_idx)
    
    return similarity_df


def get_sim_matrix(root,dt_name):
    df = pd.read_csv(root+dt_name)
    
    df = prepro(df)
    
    sim_mat = make_mat(df)
    
    return sim_mat
    
if __name__ == "__main__":
    
    save_option = 0
    root = './Data/'
    dt_name = "CJ_master.csv"

    sim_matrix = get_sim_matrix(root,dt_name)
    
    if save_option == 1:
        sim_matrix.to_csv("similarity_matrix.csv")


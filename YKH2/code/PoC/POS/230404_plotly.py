import pandas as pd
from geopy.geocoders import Nominatim
import pandas as pd
import plotly.express as px


data_root = "C:/Users/kyoo02/OneDrive - Kearney/바탕 화면/2023/PJT/CJFreshWay/Code2/c_project/YKH/data/CJ_m12.csv"
data      = pd.read_csv(data_root,encoding="utf-8-sig")

def plotly_ploting(df):

    fig = px.scatter_mapbox(df, lat='lat', lon='long', hover_name='name',hover_data=['buy_real','sales_real'])
    fig.update_layout(mapbox_style = "open-street-map")
    fig.show()

ploted_map = plotly_ploting(data)
    











import folium
from sqlalchemy import create_engine
import geopandas as gpd
import json
import pyproj

# 從資料庫裡撈data
def get_data(data_name,engine):
    sql=f'select * from public.{data_name}'
    data_file=gpd.GeoDataFrame.from_postgis(sql,engine,geom_col='geom')
    # data_file.crs=4326
    return data_file

# 經緯度對調
def swap_coordinate(data):
    new_data=json.loads(data)
    for d in new_data['features']:
        d['geometry']['coordinates'][0],d['geometry']['coordinates'][1]=d['geometry']['coordinates'][1],d['geometry']['coordinates'][0]
    return new_data

# 創建地圖
def create_map(coordinate=(22.62516116466572, 120.29979192527767)):
    map=folium.Map(coordinate,tiles="Cartodb Positron",zoom_start=12,control_scale=True)
    return map

# 增加geojson資料
def add_data(data_name,map_name,engine):
    folium.GeoJson(
        get_data(data_name,engine).to_json(),
        name=data_name,
        popup="test"
    ).add_to(map_name)


def search(data_name,search_name,engine):
    data=get_data(data_name,engine)
    data=data[data['名稱']==search_name]
    return data

if __name__=='__main__':
    pyproj.datadir.set_data_dir('C:\\Users\\godsp\\anaconda3\\envs\\geo_env\\Library\\share\\proj')
    engine=create_engine('postgresql://postgres:5733@localhost:5432/testing')
    map=create_map()
    add_data('高雄市私立托嬰中心名冊',map)
    map.save(r"web\templates\map.html")
    


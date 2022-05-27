import folium
from sqlalchemy import create_engine
import geopandas as gpd
import json
import pyproj

def get_data(data_name,engine):
    """從資料庫裡撈data，data_name是資料庫裡的table名稱，engine是串接資料庫的接口"""
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

# 創建初始化地圖
def create_map(coordinate=(22.62516116466572, 120.29979192527767)):
    map=folium.Map(coordinate,tiles="Cartodb Positron",zoom_start=12,control_scale=True)
    return map


def add_data_from_sql(data_name,map_name,engine):
    """從資料庫中撈data轉成geojson資料匯入地圖上"""
    folium.GeoJson(
        get_data(data_name,engine).to_json(),
        name=data_name
    ).add_to(map_name)


def search(data_name,filter,search_name,engine):
    """從資料庫中撈data，並回傳資料"""
    data=get_data(data_name,engine)
    data=data[data[filter]==search_name]
    return data

if __name__=='__main__':
    pyproj.datadir.set_data_dir('C:\\Users\\godsp\\anaconda3\\envs\\geo_env\\Library\\share\\proj')
    engine=create_engine('postgresql://postgres:5733@localhost:5432/testing')
    map=create_map()
    map.save(r"web\templates\map.html")
    


# -*- coding: UTF-8 -*-
# flask
from flask import Flask
from flask import render_template
from flask import request

# insert map
import folium
from numpy import NaN
# import sql
from sqlalchemy import create_engine
# import geo_tool
import pyproj
import geopandas as gpd
#import pkg
import map_set
import time

app = Flask(__name__, static_folder='static', static_url_path='/')



@app.route('/')
def index():
    map=map_set.create_map()
    map_set.add_data_from_sql('高雄市社會住宅點位',map,engine)
    map.save(r"web\templates\map.html")
    return render_template('homepage.html')


@app.route('/search')
def get_results():
    name = request.args.get('social_housing', '')
    data=map_set.search('高雄市社會住宅點位','名稱',name,engine)
    households_num=data['總戶數'].values[0]
    global one_room,two_room,three_room,housing_population
    one_room=data['一房型'].values[0]
    two_room=data['二房型'].values[0]
    three_room=data['三房型'].values[0]
    organizer=data['單位'].values[0]
    
    map=map_set.create_map()
    # 匯入社宅點位資料
    folium.GeoJson(
        data.to_json()
    ).add_to(map)
    
    # 社宅點位buffer500公尺
    global buffer
    data=data.to_crs(epsg=3826)
    buffer=data.buffer(500)
    buffer=buffer.to_crs(epsg=4326)
    folium.GeoJson(
        buffer.to_json()
    ).add_to(map)
    
    # zoom in 到社宅及buffer點位
    map.fit_bounds(map.get_bounds(),padding=(30,30))
    map.save(r"web\templates\map.html")

    if one_room>0 and two_room>0 and three_room>0:
        one_room=int(one_room);two_room=int(two_room);three_room=int(three_room)
        housing_population=one_room+two_room*3+three_room*4
    else:
        housing_population=False;one_room=False;two_room=False;three_room=False
    return render_template('search.html',
                            name=name,
                            households_num=int(households_num),
                            one_room=one_room,
                            two_room=two_room,
                            three_room=three_room,
                            housing_population=housing_population,
                            organizer=organizer)

@app.route('/analysis')
def analysis():
    one=int(request.args.get('one',one_room))
    two=int(request.args.get('two',two_room))
    three=int(request.args.get('three',three_room))
    sum=one+two*3+three*4
    
    # 根據計畫容納人口判斷提供的公設項目
    if sum<300:
        # 未滿300人不提供托育服務
        kid=False
    elif sum<1500:
        # 未滿1500人不提供青年創業空間
        startup=False
    
    # buffer500覆蓋到的行政區
    vill=map_set.get_data('高雄市村里界',engine=engine)

    return render_template('analysis.html',)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/spatial_set')
def set():
    return render_template('spatial_set.html')



if __name__ == '__main__':
    pyproj.datadir.set_data_dir('C:\\Users\\godsp\\anaconda3\\envs\\geo_env\\Library\\share\\proj')
    engine=create_engine('postgresql://postgres:5733@localhost:5432/testing')
    app.run(host='0.0.0.0', port=3000, debug=True)
    
    
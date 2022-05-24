# -*- coding: UTF-8 -*-
# flask
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_file

# insert map
import folium
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
    map_set.add_data('高雄市社會住宅點位',map,engine)
    map.save(r"web\templates\map.html")
    return render_template('homepage.html')


@app.route('/search')
def get_results():
    name = request.args.get('social_housing', '')
    data=map_set.search('高雄市社會住宅點位',name,engine)
    households_num=data['總戶數'].values[0]
    one_room=data['一房型'].values[0]
    two_room=data['二房型'].values[0]
    three_room=data['三房型'].values[0]
    organizer=data['單位'].values[0]
    map2=map_set.create_map()
    folium.GeoJson(
        data.to_json()
    ).add_to(map2)
    
    # add buffer
    data=data.to_crs(epsg=3826)
    buffer=data.buffer(500)
    buffer=buffer.to_crs(epsg=4326)
    folium.GeoJson(
        buffer.to_json()
    ).add_to(map2)
    
    map2.fit_bounds(map2.get_bounds(),padding=(30,30))
    map2.save(r"web\templates\map.html")
    return render_template('results.html',
                            name=name,
                            households_num=households_num,
                            one_room=one_room,
                            two_room=two_room,
                            three_room=three_room,
                            organizer=organizer)

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
    
    
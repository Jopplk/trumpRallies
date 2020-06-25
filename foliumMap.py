import pandas as pd
import folium


data2016 = pd.read_csv('data/2016Campaign/data2016.csv')
dataPost = pd.read_csv('data/postElection/dataPost.csv')

usMap = folium.Map(
    tiles='OpenStreetMap',
    location=[39.8283, -98.5795], 
    zoom_start=4.75)

data2016.apply(lambda row:folium.CircleMarker((row['latitude'], row['longitude']), 
    radius=4,
    weight=.5,
    color='blue',
    fill_color='blue',
    fill_opacity='.25').add_to(usMap), axis=1)

dataPost.apply(lambda row:folium.CircleMarker((row['latitude'], row['longitude']), 
    radius=4,
    weight=.5,
    color='red',
    fill_color='red',
    fill_opacity='.25').add_to(usMap), axis=1)

usMap.save('map.html')

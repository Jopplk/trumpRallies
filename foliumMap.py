import pandas as pd
import folium
from folium.features import Choropleth
import json


def pointMap(filename, kwargs):
    foliumMap = folium.Map(**kwargs)

    data2016 = pd.read_csv('data/2016Campaign/data2016.csv')
    dataPost = pd.read_csv('data/postElection/dataPost.csv')

    data2016.apply(lambda row: folium.CircleMarker(
        (row['latitude'], row['longitude']),
        radius=4,
        weight=.5,
        color='blue',
        fill_color='blue',
        fill_opacity='.25').add_to(foliumMap), axis=1)

    dataPost.apply(lambda row: folium.CircleMarker(
        (row['latitude'], row['longitude']),
        radius=4,
        weight=.5,
        color='red',
        fill_color='red',
        fill_opacity='.25').add_to(foliumMap), axis=1)

    foliumMap.save(filename)


def choroplethMap(filename, kwargs):
    def agg(dfFile):
        data = pd.read_csv(dfFile)
        aggData = data.groupby('State')['Venue'].count()

        return aggData

    foliumMap = folium.Map(**kwargs)

    data2016agg = agg('data/2016Campaign/data2016.csv')
    dataPostagg = agg('data/postElection/dataPost.csv')

    bothAgg = data2016agg.combine(
        dataPostagg, lambda x, y: x + y, fill_value=0)

    with open('data/us-states.json') as f:
        states = json.load(f)

    Choropleth(geo_data=states,
               # data=bothAggdf, columns=['State', 'Venue'],
               data=bothAgg,
               key_on='feature.properties.name',
               fill_color='YlGn',
               fill_opacity=.6,
               legend_name='Number of Rallies'
               ).add_to(foliumMap)

    folium.LayerControl().add_to(foliumMap)

    foliumMap.save(filename)


mapSettings = dict(
    tiles='cartodbpositron',
    location=[39.8283, -98.5795],
    zoom_start=4.75)

pointMap('pointF.html', mapSettings)
choroplethMap('choroF.html', mapSettings)

import pandas as pd
import folium
import os


PATH_2016 = 'data/2016Campaign/'
PATH_POST = 'data/postElection/'


def collectData(folderPath):
    data = pd.DataFrame()
    for file in os.listdir(folderPath):
        data = data.append(pd.read_csv(folderPath + file))

    return data


data2016 = collectData(PATH_2016)
dataPost = collectData(PATH_POST)

usMap = folium.Map(location=[39.8283, -98.5795], zoom_start=4.75)

usMap.save('map.html')

import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


PATH_2016 = 'data/2016Campaign/'
PATH_POST = 'data/postElection/'


def collectData(folderPath):
    data = pd.DataFrame()
    for file in os.listdir(folderPath):
        data = data.append(pd.read_csv(folderPath + file), ignore_index=True)

    return data


def concatColumns(df, fName):
    # For some reason f-strings no work?
    # df[fName] = [f"{df['Venue']}, {df['City']}, {df['State']}"]
    df[fName] =  df['City'] + ', ' + df['State']


data2016 = collectData(PATH_2016)
dataPost = collectData(PATH_POST)

concatColumns(data2016, 'concatAddress')
concatColumns(dataPost, 'concatAddress')

locator = Nominatim(user_agent="Personal geocoding script")
geocoder = RateLimiter(locator.geocode, min_delay_seconds=1)


def geocode_df(df, geocoderObj):
    df['location'] = df['concatAddress'].apply(geocoderObj)
    df['point'] = df['location'].apply(lambda location: tuple(location.point))
    df['finalAddress'] = df['location'].apply(lambda location: location.address)
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)


geocode_df(data2016, geocoder)
geocode_df(dataPost, geocoder)


#Special cases ----------------------
def agg(dfFile, column):
    data = pd.read_csv(dfFile)
    aggData = data.groupby(column)[column].count()

    return aggData


def fix(df, index, geoObj):
    # [:8] for Bangor, [:10] for Portland
    data = geoObj.geocode(df.at[index, 'concatAddress'][:10] + 'Maine')
    df.at[index, 'location'] = str(data)
    df.at[index, 'point'] = tuple(data.point)
    df.at[index, 'finalAddress'] = data.address
    df.at[index, 'latitude'] = tuple(data.point)[0]
    df.at[index, 'longitude'] = tuple(data.point)[1]

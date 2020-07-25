# Creates US state choropleth map with geopandas
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Getting rally data
def agg(dfFile):
    data = pd.read_csv(dfFile)
    aggData = data.groupby('State')['Venue'].count()

    return data, aggData


data2016, data2016agg = agg('data/2016Campaign/data2016.csv')
dataPost, dataPostagg = agg('data/postElection/dataPost.csv')

bothAgg = data2016agg.combine(
    dataPostagg, lambda x, y: x + y, fill_value=0)

# Converting rally coords to geopandas dataframe
bothData = data2016.append(dataPost)
geoRallyPoints = gpd.GeoDataFrame(
    bothData,
    geometry=gpd.points_from_xy(bothData.longitude, bothData.latitude))

# Getting and cleaning map shape data
path = 'data/us-states.json'
mapShape = gpd.read_file(path)

mapShape = mapShape.set_index('name')
mapShape = mapShape.drop(['AK', 'HI', 'PR'])

# Combining data
mapShape['occurances'] = bothAgg
#mapShape = mapShape.fillna(0)


### Begin Map plotting ###
# figsize=(x_inches, y_inches)
# DPI will control final export resolution

# Style Declerations
plt.rcParams["font.family"] = "Nirmala UI"
textcolor = '2e2e2e'
plt.rcParams['text.color'] = textcolor
plt.rcParams['axes.labelcolor'] = textcolor
plt.rcParams['xtick.color'] = textcolor
plt.rcParams['ytick.color'] = textcolor

fig, ax = plt.subplots(1, figsize=(8, 5))

ax.axis('off')
ax.set_aspect('equal')
ax.set_title('Number of Trump Rallies by State',
             fontsize=36)

# Create colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="3.5%", pad=0.05)

segs = 8
colors = plt.cm.get_cmap('OrRd', segs)

mappable = mpl.cm.ScalarMappable(cmap=colors)
mappable.set_array([])
mappable.set_clim(-0.5, segs + 0.5)  # Controlls tick positioning
cbar = fig.colorbar(mappable, cax=cax, orientation='horizontal')

cbar.set_ticks(np.linspace(0, segs, segs))
cbar.set_ticklabels([5, 10, 15, 20, 25, 30, 35, 40])
cbar.ax.tick_params(labelsize=16)

# Create plots
mapShape.plot(
    missing_kwds={'color': 'lightgrey'},
    ax=ax,
    column='occurances',
    cmap=colors,
    linewidth=0.8,
    edgecolor='0.8')

geoRallyPoints.plot(
    ax=ax,
    alpha=.75,
    marker='o',
    color='grey',
    markersize=26)

plt.show()

fig.savefig("map.png", dpi=300)

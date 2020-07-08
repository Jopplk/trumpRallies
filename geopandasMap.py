import geopandas as gpd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def agg(dfFile):
    data = pd.read_csv(dfFile)
    aggData = data.groupby('State')['Venue'].count()

    return aggData


path = 'data/us-states.json'

mapShape = gpd.read_file(path)

data2016agg = agg('data/2016Campaign/data2016.csv')
dataPostagg = agg('data/postElection/dataPost.csv')

bothAgg = data2016agg.combine(
    dataPostagg, lambda x, y: x + y, fill_value=0)

#bothAgg = bothAgg.rename(columns={'State': 'name'})

mapShape = mapShape.set_index('name')
mapShape = mapShape.drop(['AK', 'HI', 'PR'])

mapShape['occurances'] = bothAgg
mapShape = mapShape.fillna(0)

### Begin Map plotting ###
# figsize=(x_inches, y_inches)
# DPI will control final export resolution
fig, ax = plt.subplots(1, figsize=(9, 5))

colors = 'Reds'

ax.axis('off')
ax.set_title('# of Trump Rallies', )

# Create colorbar
nomalizeObj = matplotlib.colors.Normalize(
    vmin=mapShape['occurances'].min(),
    vmax=mapShape['occurances'].max())
fig.colorbar(matplotlib.cm.ScalarMappable(
    norm=nomalizeObj,
    cmap=colors))

mapShape.plot(
    ax=ax,
    column='occurances',
    cmap=colors,
    linewidth=0.8,
    edgecolor='0.8')

plt.show()

fig.savefig("map.png", dpi=500)

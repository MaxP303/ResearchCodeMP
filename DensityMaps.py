import dask.dataframe as dd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point
import contextily as ctx

# Load the data using Dask
input_csv_file = r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinalDD.csv"
df = dd.read_csv(input_csv_file)

# Define a function to create the geometry column
def create_geometry(df):
    df['geometry'] = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    return df

# Create a metadata DataFrame that includes the geometry column
meta = df.head(0)
meta['geometry'] = gpd.GeoSeries(dtype='geometry')

# Apply the function using map_partitions with updated meta
df_with_geometry = df.map_partitions(create_geometry, meta=meta)

# Convert to GeoDataFrame and set the CRS
gdf = gpd.GeoDataFrame(df_with_geometry.compute(), geometry='geometry')
gdf.set_crs(epsg=4326, inplace=True)  # Set the CRS to WGS84 (EPSG:4326)

# Plot the KDE map for total_oi
plt.figure(figsize=(12, 10))
kde = sns.kdeplot(x=gdf['Longitude'], y=gdf['Latitude'], weights=gdf['total_oi'],
                  cmap="hot", fill=True, bw_adjust=0.6, alpha=0.7, thresh=0.01)
ctx.add_basemap(plt.gca(), crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
plt.title('Density Map: Open Innovation (OI)')
plt.axis('off')
plt.colorbar(kde.collections[0], label='Density')
plt.savefig(r"D:\Documents\ThesisD\Run13\kde_map_total_oi.png")  # Change this file name if needed
plt.close()

# Plot the KDE map for total_ce
plt.figure(figsize=(12, 10))
kde = sns.kdeplot(x=gdf['Longitude'], y=gdf['Latitude'], weights=gdf['total_ce'],
                  cmap="hot", fill=True, bw_adjust=0.6, alpha=0.7, thresh=0.01)
ctx.add_basemap(plt.gca(), crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
plt.title('Density Map: Circular Economy (CE)')
plt.axis('off')
plt.colorbar(kde.collections[0], label='Density')
plt.savefig(r"D:\Documents\ThesisD\Run13\kde_map_total_ce.png")  # Change this file name if needed
plt.close()

import geopandas as gpd
import pandas as pd
from libpysal.weights import KNN
from esda.moran import Moran_Local
import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load your CSV file
input_csv_file = r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinalDD.csv"
data = pd.read_csv(input_csv_file)

# Step 2: Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.Longitude, data.Latitude))

# Step 3: Set the coordinate reference system (CRS) to WGS84 (EPSG:4326)
gdf.crs = "EPSG:4326"

# Step 4: Calculate KNN spatial weights (choose a k value, e.g., k=10)
k_value = 15
weights = KNN.from_dataframe(gdf, k=k_value)

# Step 5: Calculate Local Moran's I for total_oi and total_ce
lisa_oi = Moran_Local(gdf['total_oi'], weights)
lisa_ce = Moran_Local(gdf['total_ce'], weights)

# Step 6: Append LISA scores and statistical significance to the GeoDataFrame
gdf['lisa_oi'] = lisa_oi.Is
gdf['p_value_oi'] = lisa_oi.p_sim
gdf['significant_oi'] = gdf['p_value_oi'] < 0.05  # Assuming a 5% significance level

gdf['lisa_ce'] = lisa_ce.Is
gdf['p_value_ce'] = lisa_ce.p_sim
gdf['significant_ce'] = gdf['p_value_ce'] < 0.05  # Assuming a 5% significance level

# Step 7: Identify High-High Clusters
mean_total_oi = gdf['total_oi'].mean()
gdf['HH_cluster_oi'] = ((gdf['lisa_oi'] > 0) &  # Positive spatial autocorrelation
                        (gdf['total_oi'] > mean_total_oi) &  # Higher than global mean
                        gdf['significant_oi'])  # Statistically significant

mean_total_ce = gdf['total_ce'].mean()
gdf['HH_cluster_ce'] = ((gdf['lisa_ce'] > 0) &  # Positive spatial autocorrelation
                        (gdf['total_ce'] > mean_total_ce) &  # Higher than global mean
                        gdf['significant_ce'])  # Statistically significant

# Step 8: Identify Combined High-High Clusters
gdf['HH_cluster_combined'] = gdf['HH_cluster_oi'] & gdf['HH_cluster_ce']

# Step 9: Plot the High-High Clusters for OI, CE, and Combined in Separate Files

# Plot for High-High Clusters of Total OI
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf[gdf['HH_cluster_oi']].plot(ax=ax, 
                               column='lisa_oi', 
                               cmap='YlOrRd', 
                               markersize=gdf['lisa_oi']*75,  # Adjust marker size based on LISA score
                               alpha=0.5, 
                               legend=True)
ctx.add_basemap(ax, source="https://tile.openstreetmap.org/{z}/{x}/{y}.png", crs=gdf.crs)
ax.set_title("High-High Clusters for Total OI")
plt.savefig(r"D:\Documents\ThesisD\Run13\high_high_clusters_oi.png", dpi=800, bbox_inches='tight')

# Plot for High-High Clusters of Total CE
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf[gdf['HH_cluster_ce']].plot(ax=ax, 
                               column='lisa_ce', 
                               cmap='YlOrRd', 
                               markersize=gdf['lisa_ce']*75,  # Adjust marker size based on LISA score
                               alpha=0.5, 
                               legend=True)
ctx.add_basemap(ax, source="https://tile.openstreetmap.org/{z}/{x}/{y}.png", crs=gdf.crs)
ax.set_title("High-High Clusters for Total CE")
plt.savefig(r"D:\Documents\ThesisD\Run13\high_high_clusters_ce.png", dpi=800, bbox_inches='tight')

# Plot for Combined High-High Clusters (Both OI and CE)
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf[gdf['HH_cluster_combined']].plot(ax=ax, 
                                     column='lisa_oi',  # Could be any column since both are High-High
                                     cmap='YlOrRd', 
                                     markersize=gdf['lisa_oi']*75,  # Adjust marker size based on LISA score
                                     alpha=0.5, 
                                     legend=True)
ctx.add_basemap(ax, source="https://tile.openstreetmap.org/{z}/{x}/{y}.png", crs=gdf.crs)
ax.set_title("Combined High-High Clusters for OI and CE")
plt.savefig(r"D:\Documents\ThesisD\Run13\high_high_clusters_combined.png", dpi=800, bbox_inches='tight')


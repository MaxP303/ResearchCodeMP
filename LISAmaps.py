import geopandas as gpd
import pandas as pd
from libpysal.weights import KNN
from esda.moran import Moran_Local
import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load your CSV file
input_csv_file = r"D:\Documents\ThesisD\first2000with_outliers_data.csv"
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

# Step 8: Plot the High-High Clusters with Color Gradient and Adjustments
fig, ax = plt.subplots(1, 2, figsize=(20, 10))

# Plotting the High-High clusters for total_oi with color gradient and varying size
gdf[gdf['HH_cluster_oi']].plot(ax=ax[0], 
                               column='lisa_oi', 
                               cmap='YlOrRd', 
                               markersize=gdf['lisa_oi']*75,  # Adjust marker size based on LISA score
                               alpha=0.99, 
                               legend=True)

ctx.add_basemap(ax[0], source="https://tile.openstreetmap.org/{z}/{x}/{y}.png", crs=gdf.crs)
ax[0].set_title("High-High Clusters for Total OI")

# Plotting the High-High clusters for total_ce with color gradient and varying size
gdf[gdf['HH_cluster_ce']].plot(ax=ax[1], 
                               column='lisa_ce', 
                               cmap='Blues', 
                               markersize=gdf['lisa_ce']*75,  # Adjust marker size based on LISA score
                               alpha=0.99, 
                               legend=True)

ctx.add_basemap(ax[1], source="https://tile.openstreetmap.org/{z}/{x}/{y}.png", crs=gdf.crs)
ax[1].set_title("High-High Clusters for Total CE")

plt.show()

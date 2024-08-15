import pandas as pd
import numpy as np
import dask.dataframe as dd
from libpysal.weights import KNN
import geopandas as gpd
from shapely.geometry import Point
from esda.moran import Moran

# Load your data with Dask
data = dd.read_csv(r"D:\Documents\ThesisD\Cronbach_trimmed_geodatafinalDD.csv")

# Convert to a Pandas DataFrame to integrate with GeoPandas (if the data is small enough)
data = data.compute()

# Create a GeoDataFrame
geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Construct a spatial weights matrix using K-Nearest Neighbors (k=15)
knn_weights = KNN.from_dataframe(gdf, k=15)

# Row-standardize the weights matrix
knn_weights.transform = 'R'

# Define the variables of interest
y_total_ce = np.array(gdf['total_ce'])  # Dependent variable: total_ce
y_total_oi = np.array(gdf['total_oi'])  # Independent variable: total_oi

# Calculate Moran's I for total_ce
moran_total_ce = Moran(y_total_ce, knn_weights)
print("Moran's I for total_ce:", moran_total_ce.I)
print("Expected I for total_ce:", moran_total_ce.EI)
print("Variance of I for total_ce:", moran_total_ce.VI_norm)
print("Z-score for total_ce:", moran_total_ce.z_norm)
print("P-value for total_ce:", moran_total_ce.p_norm)

print("\n" + "="*40 + "\n")  # Separator for clarity

# Calculate Moran's I for total_oi
moran_total_oi = Moran(y_total_oi, knn_weights)
print("Moran's I for total_oi:", moran_total_oi.I)
print("Expected I for total_oi:", moran_total_oi.EI)
print("Variance of I for total_oi:", moran_total_oi.VI_norm)
print("Z-score for total_oi:", moran_total_oi.z_norm)
print("P-value for total_oi:", moran_total_oi.p_norm)

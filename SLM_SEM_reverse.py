import pandas as pd
import numpy as np
import dask.dataframe as dd
from libpysal.weights import KNN
from spreg import GM_Lag, GM_Error
import geopandas as gpd
from shapely.geometry import Point
from scipy.sparse import csc_matrix, diags

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

# Define the dependent and independent variables using numpy arrays (instead of Dask arrays)
y = np.array(gdf['total_oi']).reshape(-1, 1)  # Dependent variable: total_oi
X = np.array(gdf[['total_ce']])  # Independent variable: total_ce

# Spatial Lag Model
print("Spatial Lag Model (SLM) Results:")
slm_model = GM_Lag(y, X, w=knn_weights, name_y='total_oi', name_x=['total_ce'], name_w='knn_weights')
print(slm_model.summary)

# Calculate robust standard errors for SLM using scipy sparse matrices
residuals = slm_model.u
X_design = csc_matrix(slm_model.x)

# Create the diagonal matrix for the residuals
D = diags(residuals.flatten()**2)

# Perform matrix multiplication and inversion for robust covariance calculation
XTX = X_design.T @ X_design
XTX_inv = np.linalg.inv(XTX.toarray())
XTDX = X_design.T @ D @ X_design

# Calculate the robust covariance matrix
robust_cov = XTX_inv @ XTDX @ XTX_inv

# Calculate robust standard errors
robust_se = np.sqrt(np.diag(robust_cov))

print("\nRobust Standard Errors for SLM:")
for i, se in enumerate(robust_se):
    print(f"Robust SE for coefficient {slm_model.name_x[i]}: {se}")

# Spatial Error Model
print("\nSpatial Error Model (SEM) Results:")
sem_model = GM_Error(y, X, w=knn_weights, name_y='total_oi', name_x=['total_ce'], name_w='knn_weights')
print(sem_model.summary)

# Calculate robust standard errors for SEM using scipy sparse matrices
residuals_sem = sem_model.u
X_design_sem = csc_matrix(sem_model.x)
D_sem = diags(residuals_sem.flatten()**2)

# Perform matrix multiplication and inversion for robust covariance calculation for SEM
XTX_sem = X_design_sem.T @ X_design_sem
XTX_inv_sem = np.linalg.inv(XTX_sem.toarray())
XTDX_sem = X_design_sem.T @ D_sem @ X_design_sem

# Calculate the robust covariance matrix for SEM
robust_cov_sem = XTX_inv_sem @ XTDX_sem @ XTX_inv_sem

# Calculate robust standard errors for SEM
robust_se_sem = np.sqrt(np.diag(robust_cov_sem))

print("\nRobust Standard Errors for SEM:")
for i, se in enumerate(robust_se_sem):
    print(f"Robust SE for coefficient {sem_model.name_x[i]}: {se}")

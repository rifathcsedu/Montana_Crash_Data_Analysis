import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_species_distributions
from sklearn.datasets.species_distributions import construct_grids
from pylab import *
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.neighbors.kde import KernelDensity
import random
import pandas as pd
import csv



try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False

    
    
lats, lons = [], []
with open('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/Montana_All_Data.csv') as f:
    reader = csv.reader(f)
    next(reader) # Ignore the header row.
    for row in reader:
        lat = float(row[15])
        lon = float(row[16])
        # filter lat,lons to (approximate) map view:
        lats.append(lat)
        lons.append(lon)
d = pd.read_csv('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/Montana_All_Data.csv')
    #Filter for events with locations. 
geolocated = d.dropna(subset = ['LATITUDE', 'LONGITUDE']) 
idxs = (geolocated['LATITUDE'] > min_lat) & (geolocated['LATITUDE'] < max_lat) 
idxs = idxs &  (geolocated['LONGITUDE'] > min_lon) & (geolocated['LONGITUDE'] < max_lon) 
geolocated = geolocated.loc[idxs]
# Get matrices/arrays of species IDs and locations
min_lat =  44.36338-1
max_lat = 49.00085+1
min_lon = -116.0491-1
max_lon = -104.0396+1
cmap = 'bwr'
n_neighbors = 20
res = .2

model = KernelDensity(kernel='gaussian', bandwidth = 0.4).fit(geolocated[['LATITUDE', 'LONGITUDE']])
#print(geolocated[['LATITUDE', 'LONGITUDE']])
x = np.arange(min_lat, max_lat, res)
y = np.arange(min_lon, max_lon, res)
X, Y = meshgrid(x, y)
numel = len(X) * len(X[0, :])
#print(X.shape)
#print(Y)
color_min = None
color_max = None
unraveled_x = X.reshape([numel, 1])
unraveled_y = Y.reshape([numel, 1])
#print(unraveled_x.shape)
##print(unraveled_y.shape)
data_to_eval = np.hstack([unraveled_x, unraveled_y])
#print(data_to_eval.shape)

temp=model.score_samples(data_to_eval)
#print(data_to_eval)
#density = model.predict_proba(data_to_eval)[:, 1]
density = np.exp(temp)
figure(figsize = [20, 10])    
m = Basemap(lon_0=-110.428794,lat_0=46.998846,llcrnrlat = min_lat, urcrnrlat = max_lat, llcrnrlon = min_lon, urcrnrlon=max_lon, resolution='l', fix_aspect = False)
density = density.reshape(X.shape)
print(Y)

contourf(Y, X, density)
m.drawcoastlines(linewidth = 2)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 2)
colorbar()
title("Montana Crash Data Using Kernel Density Estimator")
#show()
savefig('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/KDEMontanaCrashData.jpg')
close()

import csv
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# load earthquake epicenters:
# http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.csv

# Use orthographic projection centered on California with corners
# defined by number of meters from center position:
m  = Basemap(projection='ortho',lon_0=-110.428794,lat_0=46.998846,resolution='c',\
             llcrnrx=-800*600,llcrnry=-800*400,
             urcrnrx=+600*900,urcrnry=+450*600)
m.drawcoastlines()
m.drawcountries()
m.drawstates()
lats, lons = [], []
with open('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/Gallatin_notowns_All_Data.csv') as f:
    reader = csv.reader(f)
    next(reader) # Ignore the header row.
    for row in reader:
        lat = float(row[15])
        lon = float(row[16])
        # filter lat,lons to (approximate) map view:
        lats.append( lat )
        lons.append( lon )
#print(lats)
#print (lons)




# define custom colormap, white -> nicered, #E6072A = RGB(0.9,0.03,0.16)


#plt.clim([0,100])


# translucent blue scatter plot of epicenters above histogram:    
x,y = m(lons, lats)
m.plot(x, y, 'o', markersize=5,zorder=6, markerfacecolor='Red',markeredgecolor="none", alpha=0.33)
 
    
# http://matplotlib.org/basemap/api/basemap_api.html#mpl_toolkits.basemap.Basemap.drawmapscale
    
    
# make image bigger:
plt.gcf().set_size_inches(25,25)

#plt.show()
plt.savefig('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/MontanaCrashData.jpg')
plt.close()

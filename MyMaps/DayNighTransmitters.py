import csv

# Open the earthquake data file.
filename = 'transmitter_info.csv'
# Create empty lists for the latitudes and longitudes.
lats, lons, labels, tunlon, tunlat = [], [], [], [], []

# Read through the entire file, skip the first line,
#  and pull out just the lats and lons.
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)
    
    # Ignore the header row.
    next(reader)
    
    # Store the latitudes and longitudes in the appropriate lists.
    for row in reader:
        labels.append(row[0])
        lats.append(float(row[1]))
        lons.append(float(row[2]))
        tunlon.append(float(row[4]))
        tunlat.append(float(row[5]))
#Tunis coordinate
tunis_lat=36.5
tunis_lon=10.08
# --- Build Map ---
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#from matplotlib.widgets import Cursor
import numpy as np
from datetime import datetime
map = plt.figure(figsize=[7,5]) 
map = Basemap(projection='mill', area_thresh = 1000.0,
              lat_0=0, lon_0=10, resolution = 'l', suppress_ticks=True)      #resolution : 'l' for low and 'h' for hight and 'c'


map.drawcoastlines()
map.drawcountries()
map.drawmapboundary(fill_color='lightblue')
map.fillcontinents(color='#FFD39B',lake_color='lightblue')
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
 
x,y = map(lons, lats)
v,w = map(tunis_lon, tunis_lat)
map.plot(x, y, 'ro', markersize=7, label='VLF transmitters')
map.plot(v, w, 'y^', markersize=7, label='LSAMA-Tunisia')
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, label, color='purple',fontsize=10, fontweight='bold')

for wpt, vpt, xpt, ypt in zip(tunlon, tunlat, lons, lats):
    # draw great circle route between tunisia and vlf trx
   
    map.drawgreatcircle(wpt,vpt,xpt,ypt,linewidth=1, color='r')
    
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.today()
CS=map.nightshade(date)
plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))

#to show long/lat coordination under the curosor
ax = plt.gca()
def format_coord(x, y):
    return 'Longitude=%.4f, Latitude=%.4f'%(map(x, y, inverse = True))
ax.format_coord = format_coord

#cursor
## set useblit = True on gtkagg for enhanced performance
#cursor = Cursor(ax, useblit=True, color='yellow', linewidth=1 )

#make legend
legend = plt.legend(loc='lower left',fontsize=8,frameon=True,title='Legend',markerscale=1,prop={'size':10})
legend.get_title().set_fontsize('20')

plt.show()

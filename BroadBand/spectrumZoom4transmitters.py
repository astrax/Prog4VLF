import wave
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

filename='Tunisia-2016-03-01-01-00-00-0.wav'
time= str(filename[-14:-12]) + ':' + str(filename[-11:-9]) + ':' + str(filename[-8:-6])
date= str(filename[-17:-15]) + '-' + str(filename[-20:-18]) + '-' + str(filename[-25:-21])
if filename[-5:-4]=='0':
    CH='NS'
else:
    CH='EW'
station = str(filename[-33:-26])

spf = wave.open(filename,'r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()
#If Stereo
if spf.getnchannels() == 2:
    print ('Just mono files')
    sys.exit(0)

Time=np.linspace(0, len(signal)/fs, num=len(signal))
fig, ax = plt.subplots(figsize=(10, 5), facecolor='white',dpi=100)
spec=ax.specgram(signal, NFFT=1024, noverlap=300, Fs=fs, cmap=plt.cm.jet,vmin=-25, interpolation='sinc') #noverlap=250 for low resolution 
#and noverlap=450 for hight resolution, cmap=plt.cm.viridis

ax.set_xlim(0., 60)
ax.set_ylim(0, 50000)
ax.set_title(station + ', ' + date + ', ' + CH, fontsize=18, weight='bold')
ax.set_xlabel("Seconds after " + time + " UT", fontsize=16, weight='bold')
ax.set_ylabel("Frequency (Hz)", fontsize=16, weight='bold')

#axcb=plt.colorbar(pad=0.05,shrink=1,extendrect=True)
#axcb.set_label('dB', fontsize=14, weight='bold')

axins = zoomed_inset_axes(ax, 6, loc=1)  # zoom = 6
axins.specgram(signal, NFFT=1024, noverlap=300, Fs=fs, cmap=plt.cm.jet,vmin=-25, interpolation='sinc')

# sub region of the original image
x1, x2, y1, y2 = 10, 13, 18400, 25000
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

plt.xticks(visible=False)
plt.yticks(visible=False)

# draw a bbox of the region of the inset axes in the parent axes and
# connecting lines between the bbox and the inset axes area
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

plt.savefig(filename[:-4] + '.pdf')
plt.show()

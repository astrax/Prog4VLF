# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 22:47:40 2016

@author: ahmed
"""

import os
directory = os.chdir('data/')
import scipy.io as matlab
import matplotlib.pyplot as plt
import numpy as np

#Ampfilename= raw_input('Write de name of AWESOME narrow band data: ')
Ampfilename = 'TN160924000000ICV_000A.mat'
Phifilename = 'TN160924000000ICV_000B.mat'
station= Ampfilename[14:17]
mat_a = matlab.loadmat(Ampfilename, struct_as_record=False, squeeze_me=True)
mat_p = matlab.loadmat(Phifilename, struct_as_record=False, squeeze_me=True)
amp = mat_a['data']
phi =mat_p['data']
fsL = mat_a['Fs']
year = mat_a['start_year']

month= mat_a['start_month']
day = mat_a['start_day']
hr = mat_a['start_hour']
mn = mat_a['start_minute']
sec= mat_a['start_second']

Tstart = [float(year),float(month),float(day),float(hr),float(mn),float(sec)] # vector of time.
#print Tstart
S= np.array([1, 1/60., 1/3600.]) * Tstart[3:6]
startTime =S.sum(axis=0) # star time in hours
#print startTime


step =[]
tLo= []
for i in range(0, len(amp), 1):
    t = i
    step.append(t)
    t1= startTime + (step[i]/float(fsL)/3600.)
    #print (t1)
    tLo.append(t1)
    


f = open("%s%s%s%s.txt"%(year,month,day,station), 'w')
f.write("# time  Amplitude  Phase\n")
for i in range(0,len(tLo)-1):
    f.write(str(tLo[i]) + " " + str(amp[i]) + " " + str(phi[i]) + "\n")

f.close()


ax1=plt.subplot(2, 1, 1)
plt.grid()
plt.plot(tLo, 20*np.log10(amp), '-b')
ax1.set_ylabel('Amplitude [dB]', fontsize=12)
ax1.set_xticks([])
#plt.xlabel('Time (UT)', fontsize=12)
ax1.set_title ('Tunisia %.0f-%.0f-%.0f %s Amplitude'%(float(year),float(month),float(day),station),
           fontsize=14, weight='bold')


ax2=plt.subplot(2, 1, 2, sharex=ax1)
ax2.grid()
ax2.plot(tLo[:len(phi)], phi, '-b')
ax2.set_ylabel(r'Phase [$^\circ$]', fontsize=12)
ax2.set_xlabel('Time (UT)', fontsize=12)
ax2.set_title ('Tunisia %.0f-%.0f-%.0f %s Phase'%(float(year),
                                               float(month),
                                               float(day),station),
           fontsize=14, weight='bold')

plt.show()

import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_Cleo_2mm.pickle", "rb") #This thing reads the data proccessed in other scripts
data2 = pickle.load(pickle_in)

pickle_in = open("sensitivity_Cleo_5mm.pickle", "rb")
data5 = pickle.load(pickle_in)



fig = plt.figure()
ax = fig.add_subplot()

plt.plot(1e-3*data2['TRACE01'][:-1, 0], 1e6*data2['Bmin1'][:-1], linestyle='-', color='black', label='far')
plt.plot(1e-3*data2['TRACE01'][:-1, 0], 1e6*data2['Bmin2'][:-1], linestyle='-', color='blue', label='2 mm')
plt.plot(1e-3*data5['TRACE03'][:-1, 0], 1e6*data5['Bmin5'][:-1], linestyle='-', color='red', label='5 mm')

plt.yscale('log')
plt.legend(loc='lower right')
# ax2.legend(loc='upper left')
plt.xlabel('Frequency (kHz)', fontsize='18')
plt.ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)', fontsize='18')
plt.title('Sensitivity comparison', fontsize='18')
plt.xlim(0, 1000)
plt.tight_layout()
ax.xaxis.set_major_locator(plt.MultipleLocator(200))#This controls the interval of the x-axis ticks. In this case is 200 kHz
ax.tick_params(axis='x', direction='in', width=1, labelsize=16)
ax.tick_params(axis='y', direction='in', width=1, labelsize=16)
ax.tick_params(axis='y', which='minor', direction='in', width=1)
for axis in ['top', 'bottom', 'left', 'right']:#Control thickness of the axis lines
    ax.spines[axis].set_linewidth(1.5)

plt.show()

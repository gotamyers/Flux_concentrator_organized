import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_Cleo_2mm.pickle", "rb")
data2 = pickle.load(pickle_in)

pickle_in = open("sensitivity_Cleo_5mm.pickle", "rb")
data5 = pickle.load(pickle_in)




plt.figure(1)

plt.plot(1e-3*data2['TRACE01'][:-1, 0], 1e6*data2['Bmin1'][:-1], linestyle='-', color='blue', label='far')
plt.plot(1e-3*data2['TRACE01'][:-1, 0], 1e6*data2['Bmin2'][:-1], linestyle='-', color='black', label='2 mm')
plt.plot(1e-3*data5['TRACE03'][:-1, 0], 1e6*data5['Bmin5'][:-1], linestyle='-', color='red', label='5 mm')

plt.yscale('log')
plt.legend(loc='lower right')
# ax2.legend(loc='upper left')
plt.xlabel('Frequency (kHz)')
plt.ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)')
plt.title('Sensitivity comparison')
plt.xlim(100, 1000)

plt.show()

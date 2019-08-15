import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("simple_sensitivity_2mm.pickle", "rb")
data = pickle.load(pickle_in)

'''Plot graph'''
xmin = data['TRACE01'][:, 0].min()
xmax = data['TRACE01'][:, 0].max()

'''Plot 1'''
#fig = plt.fig()
ax = plt.axes()
plt.plot(data['TRACE01'][:, 0]/1e6, 1e6*data['Bmin_550_9dBm_far'], label='550_far')
plt.plot(data['TRACE01'][:, 0]/1e6, 1e6*data['Bmin_150_9dBm_far'], label='150_far')
plt.plot(data['TRACE01'][:, 0]/1e6, 1e6*data['Bmin_550_9dBm_close'], label='550_close')
plt.plot(data['TRACE01'][:, 0]/1e6, 1e6*data['Bmin_150_9dBm_close'], label='150_close')
ax.set_xlim([0.1, 1])

# plt.plot('x', 'y3', marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
plt.legend(loc='upper left')
plt.xlabel('Frequency (MHz)')
plt.ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)')

plt.show()
########################################################################################################################



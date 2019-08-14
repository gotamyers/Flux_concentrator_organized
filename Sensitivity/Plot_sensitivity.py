import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("absolute_sensitivity_2mm.pickle", "rb")
data = pickle.load(pickle_in)

'''Plot graph'''
xmin = data['TRACE01'][:, 0].min()
xmax = data['TRACE01'][:, 0].max()

'''Plot 1'''
#fig = plt.fig()
ax = plt.axes()
plt.plot(data['TRACE01'][:, 0], data['Bmin_550_9dBm_far'], label='far')
plt.plot(data['TRACE01'][:, 0], data['Bmin_550_9dBm_close'], label='close')

# plt.plot('x', 'y3', marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
plt.legend(loc='upper left')

plt.show()
########################################################################################################################



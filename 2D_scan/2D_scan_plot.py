import matplotlib.pyplot as plt
import matplotlib
import pickle
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import StrMethodFormatter
'''This script is for plotting the gain in function of the flux concentrator's
position on the x- and y- axis'''
pickle_in = open("2d_scan_2mm.pickle2", "rb")
data2 = pickle.load(pickle_in)

x = np.around(np.linspace(-0.7, 0.7, 28), decimals=2)
y = np.around(np.linspace(-0.7, 0.7, 28), decimals=2)

z = data2['TRACE_signal'].transpose()
fig, ax = plt.subplots()
plt.title('Gain of a 2 mm flux concentrator (dB)')
plt.imshow(z, origin='lower', extent=[-0.7, 0.7, -0.65, 0.7], interpolation="none")
# plt.xticks(np.arange(22), x)
# plt.yticks(np.arange(22), y)
plt.xlabel('x-position (mm)')
plt.ylabel('y-position (mm)')
# plt.locator_params(axis='y', nbins=6)

plt.colorbar()

plt.show()

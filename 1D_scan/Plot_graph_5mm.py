import matplotlib.pyplot as plt
import pickle
import numpy as np


'''This plot is better for plotting the data in function of the flux concentrator height'''
pickle_in = open("1d_scan_5mm.pickle2", "rb")
data5 = pickle.load(pickle_in)

#This is creating a 1D array for the corresponding height values
z = np.around(np.linspace(10, 130, 13), decimals=0)
z = np.append(z, np.around(np.linspace(150, 330, 10), decimals=0))
z = np.append(z, np.around(np.linspace(380, 530, 4), decimals=0))

x = np.multiply(data5['TRACE01'][:, 0], 1e-6)
xx, yy = np.meshgrid(x, z)

#Need to transpose so that We have height x frequency
data5['TRACE_signal'] = data5['TRACE_signal'].transpose()

'''Plots the graph'''
fig, ax0 = plt.subplots()
ax0.set_title('Gain dependence with height for a 5 mm flux conc. (dB)')
ax0.set_xlabel('Frequency (MHz)')
ax0.set_ylabel('Height (um)')
plt.locator_params(axis='x', nbins=5)

c = ax0.pcolor(xx, yy, data5['TRACE_signal'], cmap='magma')
fig.colorbar(c, ax=ax0)

plt.show()

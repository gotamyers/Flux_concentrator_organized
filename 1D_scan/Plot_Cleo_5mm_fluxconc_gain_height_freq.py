import pickle
import numpy as np
import matplotlib.pyplot as plt



'''Read dictionary'''
pickle_in = open("1d_scan_5mm.pickle", "rb")
data5 = pickle.load(pickle_in)

z = np.array([10, 100, 200, 500])

freq = data5['TRACE01'][:, 0]

'''Plots the graph'''
fig, ax0 = plt.subplots()
ax0.plot(1e-6*data5['TRACE01'][:, 0], data5['TRACE01'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='blue', label='10 $\mu$m')
ax0.plot(1e-6*data5['TRACE11'][:, 0], data5['TRACE11'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='red', label='100 $\mu$m')
ax0.plot(1e-6*data5['TRACE17'][:, 0], data5['TRACE17'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='green', label='200 $\mu$m')
ax0.plot(1e-6*data5['TRACE26'][:, 0], data5['TRACE26'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='black', label=r'500 $\mu$m')
ax0.set_title('Gain dependence with height for a 5 mm flux concentrator')
ax0.set_xlabel('Frequency (MHz)')
ax0.set_ylabel('Gain (dB)')

plt.legend(loc='upper right')

plt.show()


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
ax0.plot(1e-3*data5['TRACE01'][:, 0], data5['TRACE01'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='blue', label='10 $\mu$m')
ax0.plot(1e-3*data5['TRACE11'][:, 0], data5['TRACE11'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='red', label='100 $\mu$m')
ax0.plot(1e-3*data5['TRACE17'][:, 0], data5['TRACE17'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='green', label='200 $\mu$m')
ax0.plot(1e-3*data5['TRACE26'][:, 0], data5['TRACE26'][:, 1] - data5['TRACE27'][:, 1], linestyle='-', color='black', label=r'500 $\mu$m')
ax0.set_title('Gain dependence with height\n of a 5 mm flux concentrator', fontsize='18')
ax0.set_xlabel('Frequency (KHz)', fontsize='18')
ax0.set_ylabel('Gain (dB)', fontsize='18')
plt.xlim(0, 1000)
plt.tight_layout()

ax0.xaxis.set_major_locator(plt.MultipleLocator(200))
ax0.tick_params(axis='x', direction='in', width=1, labelsize=16)
ax0.tick_params(axis='y', direction='in', width=1, labelsize=16)
ax0.tick_params(axis='y', which='minor', direction='in', width=1)
for axis in ['top', 'bottom', 'left', 'right']:
    ax0.spines[axis].set_linewidth(1.5)

plt.legend(loc='upper right')

plt.show()


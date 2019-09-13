import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_high_freq_NA.pickle", "rb")
data = pickle.load(pickle_in)

pickle_in = open("sensitivity_high_freq_func_gen.pickle", "rb")
data_higher = pickle.load(pickle_in)

pickle_in = open("simple_sensitivity_2mm.pickle", "rb")
data_old = pickle.load(pickle_in)

pickle_in = open("sensitivity_old.pickle", "rb")
data_old_set = pickle.load(pickle_in)

'''Plot graph'''
xmin = data['SSA_01_noise'][:, 0].min()
xmax = data['SSA_01_noise'][:, 0].max()

'''Plot 1'''
fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

lns1 = ax1.plot([106, 142, 160, 540, 800], 1e6*data_higher['Bmin_far'], marker='o', linestyle='none', color='blue')
lns2 = ax1.plot([106, 142, 160, 540, 800], 1e6*data_higher['Bmin_close'], marker='o', linestyle='none', color='r')
lns7 = ax1.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin1'], linestyle='-', color='blue', label='far')
lns8 = ax1.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin2'], linestyle='-', color='r', label='close')

plt.yscale('log')
# plt.xscale('log')

# ax1.set_ylim([0, 20])
ax1.set_xlim([100, 1000])
# ax.set_ylim([0.0, 40])
# lns = lns1+lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc='upper left')

ax1.legend(loc='upper left')
# ax2.legend(loc='upper left')
ax1.set_xlabel('Frequency (kHz)')
ax1.set_ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)')
# ax2.set_ylabel('Power Spectrum')
# plt.title('Fixed at 550 kHz')


'''Plot 2'''
plt.figure(2)

plt.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin1'], linestyle='-', color='blue', label='far')
plt.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin2'], linestyle='-', color='r', label='close')
plt.plot(0.001*data_old['TRACE01'][:, 0], 1e6*data_old['Bmin_550_9dBm_far'], linestyle='-', color='cornflowerblue', label='far_old')
plt.plot(0.001*data_old['TRACE01'][:, 0], 1e6*data_old['Bmin_550_9dBm_close'], linestyle='-', color='lightcoral', label='close_old')

plt.yscale('log')
# plt.xscale('log')

# ax1.set_ylim([0, 20])
plt.xlim((100, 1000))
plt.legend(loc='upper right')

plt.xlabel('Frequency (kHz)')
plt.ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)')

# plt.title('Fixed at 550 kHz')

'''Plot 3'''
plt.figure(3)

plt.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin1'], linestyle='-', color='blue', label='far')
plt.plot(0.001*data['TRACE1'][:, 0], 1e6*data['Bmin2'], linestyle='-', color='r', label='close')
plt.plot(0.001*data_old_set['TRACE1'][:, 0], 1e6*data_old_set['Bmin1'], linestyle='-', color='cornflowerblue', label='far_old')
plt.plot(0.001*data_old_set['TRACE1'][:, 0], 1e6*data_old_set['Bmin2'], linestyle='-', color='lightcoral', label='close_old')

plt.yscale('log')
# plt.xscale('log')

# ax1.set_ylim([0, 20])
plt.xlim((100, 1000))
plt.legend(loc='upper right')

plt.xlabel('Frequency (kHz)')
plt.ylabel(r'Sensitivity ($\mu$T/$\sqrt{Hz}$)')

# plt.title('Fixed at 550 kHz')


plt.show()
########################################################################################################################



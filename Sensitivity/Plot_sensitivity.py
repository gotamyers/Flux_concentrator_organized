import math
import numpy as np
import pickle
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_high_freq.pickle", "rb")
data = pickle.load(pickle_in)

pickle_in = open("simple_sensitivity_2mm.pickle", "rb")
data_higher = pickle.load(pickle_in)

'''Plot graph'''
xmin = data['SSA_noise'][:, 0].min()
xmax = data['SSA_noise'][:, 0].max()

'''Plot 1'''
fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

lns1 = ax1.plot([106, 108.4, 142, 160, 540, 550, 800], 1e6*data['Bmin_far'], marker='o', linestyle='none', color='blue')
lns2 = ax1.plot([106, 108.4, 142, 160, 540, 550, 800], 1e6*data['Bmin_close'], marker='o', linestyle='none', color='r')
# lns3 = ax1.plot([106, 142, 540, 550, 800], 1e6*data['Bmin_03_far'], marker='x', linestyle='none', color='b', label='far+amp1')
# lns4 = ax1.plot([106, 142, 540, 550, 800], 1e6*data['Bmin_04_close'], marker='x', linestyle='none', color='r', label='close+amp1')
lns5 = ax1.plot([106, 108.4, 142, 160, 540, 550, 800], 1e6*data['Bmin_05_far'], marker='^', linestyle='none', color='b', label='far+amp')
lns6 = ax1.plot([106, 108.4, 142, 160, 540, 550, 800], 1e6*data['Bmin_06_close'], marker='^', linestyle='none', color='r', label='close+amp')
# lns3 = ax2.plot(data['SSA_noise'][:, 0]/1000, data['SSA_noise'][:, 1], color='k', linestyle='--', linewidth='0.2', label='noise')
lns7 = ax1.plot(0.001*data_higher['TRACE01'][:, 0], 1e6*data_higher['Bmin_550_6dBm_far'], linestyle='-', color='blue', label='far')
lns8 = ax1.plot(0.001*data_higher['TRACE01'][:, 0], 1e6*data_higher['Bmin_550_6dBm_close'], linestyle='-', color='r', label='close')

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



plt.show()
########################################################################################################################



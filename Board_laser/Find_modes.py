import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

radius = 50 #microns
mode_start = 225

data_TE = pd.read_csv('C:\\Users\\uqfgotar\\Documents\\Lumerical\\Disk\\50um_doubledisk_simulation_TE.txt', sep=",", header=None)
data_TE = data_TE.iloc[1:, :]
data_TM = pd.read_csv('C:\\Users\\uqfgotar\\Documents\\Lumerical\\Disk\\50um_doubledisk_simulation_TM.txt', sep=",", header=None)
data_TM = data_TM.iloc[1:, :]

TE = np.asarray(data_TE, dtype=np.float)
TM = np.asarray(data_TM, dtype=np.float)

wavelength = np.linspace(1554, 1556, len(TE[:, 0]))


plt.figure(1)
plt.plot(wavelength, TE[:, 1], color='steelblue', label='TE')
plt.plot(wavelength, TM[:, 1], color='firebrick', label='$n_{eff}$ TM')
for k in range(25):
    theo_neff = (mode_start + k) * wavelength / (2 * np.pi * radius * 1e3)
    plt.plot(wavelength, theo_neff, color='k', linestyle=':')

plt.legend(loc='upper right')
plt.xlabel('wavelength (nm)')
plt.ylabel('Effective index')

plt.show()

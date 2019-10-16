import csv
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mticker

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = math.sqrt(27.3 * 50 * math.pow(10, 0.8) * 1e-3)  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius
# frequencies = [10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990]
# noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for k in range(8):
    for i in range(3):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\16thOct'
                  + '\\SSA_n' + str(k) + str(i) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['noise' + str(k) + str(i)] = np.reshape(np.array(df), (-1, 2))
        data['noise' + str(k) + str(i)] = np.array(df)
        data['mean' + str(k) + str(i)] = np.mean(data['noise' + str(k) + str(i)][:, 1])
        blob = np.where((data['noise' + str(k) + str(i)] > 151000) & (data['noise' + str(k) + str(i)] < 163000))
        data['mean' + str(k) + str(i) + '6070'] = np.mean(data['noise' + str(k) + str(i)][blob, 1])

colors = ['indianred', 'darkorange', 'forestgreen', 'steelblue', 'black', 'lime', 'mediumblue', 'darkviolet']
Power = [18.3, 17.4, 16.4, 15.5, 14.4, 13.4, 12.4, 11.4]
for i in range(3):
    plt.figure(i)
    for k in range(8):
        plt.plot(data['noise' + str(k) + str(i)][:, 0], data['noise' + str(k) + str(i)][:, 1], colors[k],
                 label=str(Power[k]))
        # plt.scatter(data['mean' + str(k) + str(i)], Power[k], color='r')
    plt.legend(loc='upper right')

for i in range(3):
    plt.figure(i + 3)
    for k in range(8):
        plt.scatter(Power[k], data['mean' + str(k) + str(i) + '6070'], color='r')

plt.show()

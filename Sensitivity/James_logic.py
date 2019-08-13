import csv
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mticker

initial = time.time()  # just for counting the time it spends on this script
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

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for k in range(11):
    for i in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\25thJune_ZScan'
                  + '\\Spectrum_analyzer\\SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(k + 1) + '_exp_' + str(i)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + str(k + 1) + '_exp_' + str(i)] = np.array(df)
    data['signal' + str(k + 1)] = data['SSA_' + str(k + 1) + '_exp_1'][350:450, 1].max()
    data['noise' + str(k + 1)] = data['SSA_' + str(k + 1) + '_exp_0'][350:450, 1].max()
    data['SNR' + str(k + 1)] = data['signal' + str(k + 1)] - data['noise' + str(k + 1)]
    data['S_NN_' + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str(k + 1) + '_exp_0'][:, 1], 10))

########################################################################################################################
'''Read Network analyzer and calculate S_21 in not dB'''
for k in range(11):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\25thJune_ZScan'
              + '\\Network_analyzer\\TRACE' + str("{:02d}".format(k + 1)) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []

        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['TRACE' + str(k + 1)] = np.reshape(np.array(df), (-1, 2))

    data['S_21_' + str(k + 1)] = np.power(10, np.divide(data['TRACE' + str(k + 1)][:, 1], 10))

########################################################################################################################
'''Normalise S_NN and S_21 with the reference'''
for k in range(11):
    data['S_NN_' + str(k + 1)] = np.divide(data['S_NN_' + str(k + 1)], data['S_NN_11'])
    data['S_21_' + str(k + 1)] = np.divide(data['S_21_' + str(k + 1)], data['S_21_11'])

########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''
ymax = np.zeros(11)
for k in range(11):
    data['Bmin' + str(k + 1)] = np.sqrt(np.divide(data['S_NN_' + str(k + 1)], data['S_21_' + str(k + 1)])) * B_ref
    data['Bmin' + str(k + 1)] = np.multiply(
        np.divide(data['Bmin' + str(k + 1)], np.sqrt(np.multiply(data['SNR' + str(k + 1)], RBW))), 1e9)
    data['Bmin_min' + str(k + 1)] = data['Bmin' + str(k + 1)].min()

########################################################################################################################
'''Array for the heights we measured (z)'''
height = [20, 50, 80, 110, 140, 200, 260, 360, 500, 1000]
height = np.array(height)
########################################################################################################################

'''Plot graph'''
axes = plt.gca()
xmin = data['TRACE1'][:, 0].min()
xmax = data['TRACE1'][:, 0].max()

plt.figure(1)
for k in range(10):
    plt.plot(np.multiply(data['TRACE' + str(k + 1)][:, 0], 1e-6), data['Bmin' + str(k + 1)],
             label='$\Delta$z = ' + str(height[k]))

plt.xlabel('Frequency (MHz)')
plt.ylabel('Sensitivity ($nT$/$\sqrt{Hz}$)')
plt.yscale('log')
axes.set_xlim([(0.1), 1])
axes.set_ylim([10, 1e7])
plt.legend(loc='upper left')

'''Plot meshgrid graph'''
plt.figure(2)

x_mesh, z_mesh = np.meshgrid(np.multiply(data['TRACE1'][:, 0], 1e-6), height)
plt.scatter(x_mesh, z_mesh)
axes.set_xlim([(0.1), 1])

plt.show()
########################################################################################################################

import csv
import math
import numpy as np
import matplotlib.pyplot as plt

'''This script is used for reading, calculating and plotting absolute sentivity for the the data acquired on first week
 of August. We measured S21, SA noise and SA reference for 2 and 5 mm long flux concentrator in positions far and close
 to the magnetometer as well as for two different powers: 6 and 9 dBm + amplifier that has approximately 25 dB gain:
 9 dBm = 630 mVrms; 6 dBm = 450 mVrms. With the amp, we have a output voltage of 11.2 Vrms and 5.66 Vrms'''

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
nu_ref1 = 550 * 1e3  # Func. gen. driving freq.
nu_ref2 = 150 * 1e3  # Func. gen. driving freq.
V_drive = math.sqrt(27.3 * 50 * math.pow(10, 0.9) * 1e-3)  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven1 = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref1 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref1 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven1 / radius
I_driven2 = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref2 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref2 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven2 / radius

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for i in [0, 2, 5, 7, 8, 9]:
    for k in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\9thAug'
                  + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(i) + str(k + 1)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + str(i) + str(k + 1)] = np.array(df)

data['SSA_noise_550_9dBm_01'] = data['SSA_01'][250:430, 1].max()
data['SSA_noise_150_9dBm_01'] = data['SSA_01'][:200, 1].max()
data['SSA_noise_550_6dBm_21'] = data['SSA_01'][250:430, 1].max()
data['SSA_noise_150_6dBm_21'] = data['SSA_01'][:200, 1].max()
for i in [0, 2]:
    for k in range(2):
        data['SNN_' + str(i) + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str(i) + str(k + 1)][:, 1], 10))

for i in [5, 8]:
    for k in range(2):
        data['SSA_signal_550_' + str(i) + str(k + 1)] = data['SSA_' + str(i) + str(k + 1)][:430, 1].max()
for i in [7, 9]:
    for k in range(2):
        data['SSA_signal_150_' + str(i) + str(k + 1)] = data['SSA_' + str(i) + str(k + 1)]

for k in range(2):
    data['SNR_550_9dBm_5' + str(k + 1)] = data['SSA_signal_550_5' + str(k + 1)] - data['SSA_noise_550_9dBm_01']
    data['SNR_150_9dBm_7' + str(k + 1)] = data['SSA_signal_150_7' + str(k + 1)] - data['SSA_noise_150_9dBm_01']
    data['SNR_550_6dBm_8' + str(k + 1)] = data['SSA_signal_550_8' + str(k + 1)] - data['SSA_noise_550_6dBm_21']
    data['SNR_150_6dBm_9' + str(k + 1)] = data['SSA_signal_150_9' + str(k + 1)] - data['SSA_noise_150_6dBm_21']

# data['signal' + str(k + 1)] = data['SSA_' + str(k + 1)][350:450, 1].max()
# data['noise' + str(k + 1)] = data['SSA_' + str(k + 1)][350:450, 1].max()
# data['SNR' + str(k + 1)] = data['signal' + str(k + 1)] - data['noise' + str(k + 1)]
# data['S_NN_' + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str(k + 1)][:, 1], 10))

########################################################################################################################



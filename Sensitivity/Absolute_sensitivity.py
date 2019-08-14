import csv
import math
import numpy as np
import pickle
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
V_drive1 = math.sqrt(math.pow(10, 2.73) * 50 * math.pow(10, 0.9) * 1e-3)  # Voltage driven to the coil
V_drive2 = math.sqrt(math.pow(10, 2.73) * 50 * math.pow(10, 0.6) * 1e-3)  # Voltage driven to the coil
RBW = 30  # Resolution bandwidth
I_driven11 = V_drive1 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref1 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
I_driven12 = V_drive1 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref2 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref11 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven11 / radius
B_ref12 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven12 / radius
I_driven21 = V_drive2 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref1 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
I_driven22 = V_drive2 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref2 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref21 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven21 / radius
B_ref22 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven22 / radius

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for i in [0, 2, 5, 7, 8, 9]:
    for k in range(2):
        with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
                  + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
        # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\9thAug'
        #           + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
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
data['SSA_noise_550_9dBm_02'] = data['SSA_02'][250:430, 1].max()
data['SSA_noise_150_9dBm_01'] = data['SSA_01'][:200, 1].max()
data['SSA_noise_150_9dBm_02'] = data['SSA_02'][:200, 1].max()
data['SSA_noise_550_6dBm_21'] = data['SSA_21'][250:430, 1].max()
data['SSA_noise_550_6dBm_22'] = data['SSA_22'][250:430, 1].max()
data['SSA_noise_150_6dBm_21'] = data['SSA_21'][:200, 1].max()
data['SSA_noise_150_6dBm_22'] = data['SSA_22'][:200, 1].max()
for i in [0, 2, 5, 7, 8, 9]:
    for k in range(2):
        data['SNN_' + str(i) + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str(i) + str(k + 1)][:, 1], 10))

for i in [5, 8]:
    for k in range(2):
        data['SSA_signal_550_' + str(i) + str(k + 1)] = data['SSA_' + str(i) + str(k + 1)][:430, 1].max()
for i in [7, 9]:
    for k in range(2):
        data['SSA_signal_150_' + str(i) + str(k + 1)] = data['SSA_' + str(i) + str(k + 1)].max()


data['SNR_550_9dBm_far'] = data['SSA_signal_550_51'] - data['SSA_noise_550_9dBm_01']
data['SNR_550_9dBm_close'] = data['SSA_signal_550_52'] - data['SSA_noise_550_9dBm_02']
data['SNR_150_9dBm_far'] = data['SSA_signal_150_71'] - data['SSA_noise_150_9dBm_01']
data['SNR_150_9dBm_close'] = data['SSA_signal_150_72'] - data['SSA_noise_150_9dBm_02']
data['SNR_550_6dBm_far'] = data['SSA_signal_550_81'] - data['SSA_noise_550_6dBm_21']
data['SNR_550_6dBm_close'] = data['SSA_signal_550_82'] - data['SSA_noise_550_6dBm_22']
data['SNR_150_6dBm_far'] = data['SSA_signal_150_91'] - data['SSA_noise_150_6dBm_21']
data['SNR_150_6dBm_close'] = data['SSA_signal_150_92'] - data['SSA_noise_150_6dBm_22']
# I guess this part is finished
# data['signal' + str(k + 1)] = data['SSA_' + str(k + 1)][350:450, 1].max()
# data['noise' + str(k + 1)] = data['SSA_' + str(k + 1)][350:450, 1].max()
# data['SNR' + str(k + 1)] = data['signal' + str(k + 1)] - data['noise' + str(k + 1)]
# data['S_NN_' + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str(k + 1)][:, 1], 10))

########################################################################################################################
'''Read Network analyzer and calculate S_21 in not dB'''
for i in [0, 2]:
    for k in range(2):
        with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
                  + '\\Absolute_sensitivity_090819_FG\\TRACE' + str(i) + str(k + 1) + '.csv') as a:
        # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\9thAug'
        #           + '\\Absolute_sensitivity_090819_FG\\TRACE' + str(i) + str(k + 1) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []

            for row in df:
                df_temp.append(row)
            df = df_temp[3:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['TRACE' + str(i) + str(k + 1)] = np.reshape(np.array(df), (-1, 2))

        data['S21_' + str(i) + str(k + 1)] = np.power(10, np.divide(data['TRACE' + str(i) + str(k + 1)][:, 1], 10))

########################################################################################################################
'''Normalise S_NN and S_21 with the reference'''
for i in [0, 5, 7]:
    data['SNN_' + str(i) + str(1)] = np.divide(data['SNN_' + str(i) + str(1)], data['SNN_' + str(0) + str(1)])
    data['SNN_' + str(i) + str(2)] = np.divide(data['SNN_' + str(i) + str(1)], data['SNN_' + str(0) + str(2)])
for i in [2, 8, 9]:
    data['SNN_' + str(i) + str(1)] = np.divide(data['SNN_' + str(i) + str(1)], data['SNN_' + str(2) + str(1)])
    data['SNN_' + str(i) + str(2)] = np.divide(data['SNN_' + str(i) + str(1)], data['SNN_' + str(2) + str(2)])



data['S21_01'] = np.divide(data['S21_01'][376], data['S21_01'])
data['S21_02'] = np.divide(data['S21_02'][43], data['S21_02'])
data['S21_21'] = np.divide(data['S21_21'][376], data['S21_21'])
data['S21_22'] = np.divide(data['S21_22'][43], data['S21_22'])
#This part is also finished

########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''

data['Bmin_550_9dBm_far'] = np.sqrt(np.divide(data['SNN_51'], data['S21_01'])) * B_ref11
data['Bmin_550_9dBm_close'] = np.sqrt(np.divide(data['SNN_52'], data['S21_21'])) * B_ref11
data['Bmin_150_9dBm_far'] = np.sqrt(np.divide(data['SNN_71'], data['S21_02'])) * B_ref12
data['Bmin_150_9dBm_close'] = np.sqrt(np.divide(data['SNN_72'], data['S21_22'])) * B_ref12
data['Bmin_550_6dBm_far'] = np.sqrt(np.divide(data['SNN_81'], data['S21_21'])) * B_ref21
data['Bmin_550_6dBm_close'] = np.sqrt(np.divide(data['SNN_82'], data['S21_22'])) * B_ref21
data['Bmin_150_6dBm_far'] = np.sqrt(np.divide(data['SNN_91'], data['S21_21'])) * B_ref22
data['Bmin_150_6dBm_close'] = np.sqrt(np.divide(data['SNN_92'], data['S21_22'])) * B_ref22

data['Bmin_550_9dBm_far'] = np.multiply(np.divide(data['Bmin_550_9dBm_far'], np.sqrt(np.multiply(data['SNR_550_9dBm_far'], RBW))), 1e9)
data['Bmin_550_9dBm_close'] = np.multiply(np.divide(data['Bmin_550_9dBm_close'], np.sqrt(np.multiply(data['SNR_550_9dBm_close'], RBW))), 1e9)
data['Bmin_150_9dBm_far'] = np.multiply(np.divide(data['Bmin_150_9dBm_far'], np.sqrt(np.multiply(data['SNR_150_9dBm_far'], RBW))), 1e9)
data['Bmin_150_9dBm_close'] = np.multiply(np.divide(data['Bmin_150_9dBm_close'], np.sqrt(np.multiply(data['SNR_150_9dBm_close'], RBW))), 1e9)
data['Bmin_550_6dBm_far'] = np.multiply(np.divide(data['Bmin_550_6dBm_far'], np.sqrt(np.multiply(data['SNR_550_6dBm_far'], RBW))), 1e9)
data['Bmin_550_6dBm_close'] = np.multiply(np.divide(data['Bmin_550_6dBm_close'], np.sqrt(np.multiply(data['SNR_550_6dBm_close'], RBW))), 1e9)
data['Bmin_150_6dBm_far'] = np.multiply(np.divide(data['Bmin_150_6dBm_far'], np.sqrt(np.multiply(data['SNR_150_6dBm_far'], RBW))), 1e9)
data['Bmin_150_6dBm_close'] = np.multiply(np.divide(data['Bmin_150_6dBm_close'], np.sqrt(np.multiply(data['SNR_150_6dBm_close'], RBW))), 1e9)

data['Bmin_min_9dBm_far'] = data['Bmin_550_9dBm_far'].min()
data['Bmin_min_550_9dBm_close'] = data['Bmin_550_9dBm_close'].min()
data['Bmin_min_150_9dBm_far'] = data['Bmin_150_9dBm_far'].min()
data['Bmin_min_150_9dBm_close'] = data['Bmin_150_9dBm_close'].min()
data['Bmin_min_550_6dBm_far'] = data['Bmin_550_6dBm_far'].min()
data['Bmin_min_550_6dBm_close'] = data['Bmin_550_6dBm_close'].min()
data['Bmin_min_150_6dBm_far'] = data['Bmin_150_6dBm_far'].min()
data['Bmin_min_150_6dBm_close'] = data['Bmin_150_6dBm_close'].min()


# data['Bmin' + str(k + 1)] = np.multiply(
#     np.divide(data['Bmin' + str(k + 1)], np.sqrt(np.multiply(data['SNR' + str(k + 1)], RBW))), 1e9)
# data['Bmin_min' + str(k + 1)] = data['Bmin' + str(k + 1)].min()

########################################################################################################################
'''SAVE DICTIONARY'''
pickle_out = open("absolute_sensitivity_2mm.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
########################################################################################################################

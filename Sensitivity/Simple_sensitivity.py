import csv
import math
import numpy as np
import pickle

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
RBW = 30  # Resolution bandwidth
V_drive = math.sqrt(27.3 * 50 * math.pow(10, 0.9) * 1e-3)  # Voltage driven to the coil


########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for i in [12.4, 30, 33.64, 45, 80, 97]:
    for k in range(2):
        with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
                  + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
        # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\02ndSep'
        #           + '\\SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = np.reshape(np.array(df), (-1, 2))
        data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = np.array(df)

for i in [65, 70]:
    for k in range(2):
        # with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
        #           + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\4thSep'
                  + '\\SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = np.reshape(np.array(df), (-1, 2))
        data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = np.array(df)

with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\02ndSep'
          + '\\SSA_noise.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]

    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['SSA_noise'] = np.reshape(np.array(df), (-1, 2))
data['SSA_noise'] = np.array(df)

with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\4thSep'
          + '\\SSA_noise.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]

    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['SSA_noise2'] = np.reshape(np.array(df), (-1, 2))
data['SSA_noise2'] = np.array(df)

'''Sensitivity for flux concentrator far, applying V drive with the function generator'''
for i in [12.4, 30, 33.64, 45, 65, 70, 80, 97]:
    for k in range(2):
        data['SSA_ref_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = \
            data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'][
            int(751 * (i - 10) / 90 - 1):int(751 * (i - 10) / 90 + 1), 1].max()
        data['SSA_noise' + str(i)] = data['SSA_noise'][int(751 * (i - 10) / 90 - 1):int(751 * (i - 10) / 90 + 1), 1].max()

        data['SNR_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = \
            np.power(10, np.divide(
                data['SSA_ref_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] - data['SSA_noise' + str(i)], 10))

        data['SNN_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'] = \
            np.power(10., np.divide(data['SSA_' + str("{:02d}".format(k + 1)) + '_' + str(i) + 'khz'][:, 1], 10.))

    data['SNN_noise' + str(i)] = np.power(10., np.divide(data['SSA_noise'][:, 1], 10.))
    data['SNN_noise' + str(i)] = np.divide(data['SNN_noise' + str(i)], data['SNN_noise' + str(i)][int(751 * (i - 10) / 90)])


########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''
t = 0
data['Bmin_far'] = np.zeros(8)
data['Bmin_close'] = np.zeros(8)
for i in [12.4, 30, 33.64, 45, 65, 70, 80, 97]:
    for k in range(2):
        data['I_driven' + str(i)] = V_drive / math.sqrt(math.pow(R, 2) + math.pow((i * 1e3 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
        data['B_ref' + str(i)] = math.pow(4.5, 1.5) * mu0 * Ncoils * data['I_driven' + str(i)] / radius
        data['root_' + str("{:02d}".format(k + 1)) + '_' + str(i)] = np.sqrt(np.multiply(data['SNR_' + str("{:02d}".format(k + 1))
                                                                                                + '_' + str(i) + 'khz'], RBW))

        data['Bmin_' + str("{:02d}".format(k + 1)) + '_' + str(i)] = data['B_ref' + str(i)] / data['root_' + str("{:02d}".format(k + 1)) + '_' + str(i)]

for i in [12.4, 30, 33.64, 45, 65, 70, 80, 97]:
    data['Bmin_far'][t] = data['Bmin_01' + '_' + str(i)]
    data['Bmin_close'][t] = data['Bmin_02' + '_' + str(i)]
    t = int(i/i + t)

########################################################################################################################
'''SAVE DICTIONARY'''
pickle_out = open("sensitivity2mm.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
########################################################################################################################

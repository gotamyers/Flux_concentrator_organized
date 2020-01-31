import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import pickle

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = math.sqrt(math.pow(10, 2.73) * 50 * math.pow(10, 0.9) * 1e-3)  # Voltage driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
# I_driven11 = I_driven12 = I_driven21 = I_driven22 = 0.473
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius


########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for i in [0, 5]:
    for k in [2, 3, 5]:
        # with open('C:\\Users\\Fernando\\Documents\Phd\\7thAug'
        #           + '\\Absolute_sensitivity_080819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\7thAug'
                  + '\\AbsoluteSensitivities_080819_FG_JB\\SSA_' + str(i) + str(k) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(i) + str(k)] = np.reshape(np.array(df), (-1, 2))
        data['SSA_' + str(i) + str(k)] = np.array(df)

ind_max = np.where(data['SSA_53'][:, 1] == np.amax(data['SSA_53'][:, 1]))
# print(data['SSA_03'][ind_max, 0])
for k in [2, 3, 5]:
    data['signal' + str(k)] = data['SSA_5' + str(k)][300:450, 1].max()
    data['noise' + str(k)] = data['SSA_0' + str(k)][300:450, 1].max()
    data['SNR' + str(k)] = data['signal' + str(k)] - data['noise' + str(k)]
    data['Snn' + str(k)] = np.power(10, np.divide(data['SSA_0' + str(k)][:, 1], 10))


########################################################################################################################
'''Read NA saved data'''
for k in [2, 3, 5]:
    # with open('C:\\Users\\Fernando\\Documents\Phd\\7thAug'
    #           + '\\Absolute_sensitivity_080819_FG\\TRACE_' + str(i) + str(k + 1) + '.csv') as a:
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\7thAug'
              + '\\Absolutesensitivities_080819_FG_JB\\TRACE0' + str(k) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['TRACE0' + str(k)] = np.reshape(np.array(df), (-1, 2))
    data['TRACE0' + str(k)] = np.array(df)

    data['S21_' + str(k)] = np.power(10, np.divide(data['TRACE0' + str(k)][:, 1], 10))


'''Normalise S_NN and S_21 with the reference'''
for k in [2, 3, 5]:
    data['Snn' + str(k)] = data['Snn' + str(k)] / data['Snn' + str(k)][ind_max]
    data['S21_' + str(k)] = np.divide(data['S21_' + str(k)], data['S21_' + str(k)][ind_max])

########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''

for k in [2, 3, 5]:
    data['Bmin' + str(k)] = np.sqrt(np.divide(data['Snn' + str(k)], data['S21_' + str(k)]))*B_ref
    data['Bmin' + str(k)] = 1e6*np.divide(data['Bmin' + str(k)], np.sqrt(np.multiply(data['SNR' + str(k)], RBW)))


plt.figure(1)

plt.plot(data['TRACE03'][:-1, 0], data['Bmin2'][:-1], linestyle='-', color='blue', label='far')
plt.plot(data['TRACE03'][:-1, 0], data['Bmin5'][:-1], linestyle='-', color='black', label='close')
# plt.plot(data['TRACE03'][:-1, 0], data['Bmin53'][:-1], linestyle='-', color='red', label='close')

plt.show()
########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("sensitivity_Cleo_5mm.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################

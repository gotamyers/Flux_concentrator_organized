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
nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = 27
RBW = 30  # Resolution bandwidth
I_driven = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref * 2 * math.pi), 2) * math.pow(L, 2))
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius


########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''

for k in range(2):
    # with open('C:\\Users\\Fernando\\Documents\\Phd'
    #           + '\\sensitivity_060919_FG\\SSA_' + str('{:02d}'.format(k+1)) + '_540.csv') as a:
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\11thSep'
              + '\\SSA_' + str('{:02d}'.format(k+1)) + '_550.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[30:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['SSA_' + str('{:02d}'.format(k+1)) + '_550'] = np.reshape(np.array(df), (-1, 2))

    data['SSA_' + str('{:02d}'.format(k+1)) + '_550'] = np.array(df)
    data['SSA_' + str('{:02d}'.format(k+1)) + 'ref'] = data['SSA_' + str('{:02d}'.format(k+1))
                                                            + '_550'][360:380, 1].max()

# with open('C:\\Users\\Fernando\\Documents\\Phd'
#           + '\\sensitivity_060919_FG\\SSA_01_ref.csv') as a:
with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\11thSep'
          + '\\SSA_01.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[30:]

    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['SSA_01_noise'] = np.reshape(np.array(df), (-1, 2))

data['SSA_01_noise'] = np.array(df)
data['SSA_noise'] = data['SSA_01_noise'][360:380, 1].max()
data['S_NN_noise'] = np.power(10, np.divide(data['SSA_01_noise'][:, 1], 10))
data['S_NN_noise'] = np.divide(data['S_NN_noise'], data['S_NN_noise'][360:380].max())

'''SNR'''
for k in range(2):
    data['SNR_' + str('{:02d}'.format(k+1))] = np.power(10, np.divide(data['SSA_' + str('{:02d}'.format(k+1)) +
                                                                           'ref'] - data['SSA_noise'], 10))

########################################################################################################################
'''Read Network analyzer and calculate S_21 in not dB'''
for k in range(2):
    # with open('C:\\Users\\Fernando\\Documents\\Phd'
    #           + '\\sensitivity_060919_FG\\TRACE' + str('{:02d}'.format(k+1)) + '.csv') as a:
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\11thSep'
              + '\\TRACE' + str('{:02d}'.format(k+1)) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []

        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['TRACE' + str(k + 1)] = np.reshape(np.array(df), (-1, 2))
    data['TRACE' + str(k + 1)] = np.array(df)

    data['S21_' + str(k + 1)] = np.power(10, np.divide(data['TRACE' + str(k + 1)][:, 1], 10))
    data['S21_' + str(k + 1)] = np.divide(data['S21_' + str(k + 1)], data['S21_' + str(k + 1)][367])
    data['SSA_' + str('{:02d}'.format(k + 1)) + 'ref'] = np.power(10, np.divide(data['SSA_' + str('{:02d}'.format(k+1))
                                                                                     + 'ref'], 10))
    data['S_NN_' + str(k + 1)] = np.power(10, np.divide(data['SSA_' + str('{:02d}'.format(k+1)) + '_550'][:, 1], 10))
    data['S_NN_' + str(k + 1)] = np.divide(data['S_NN_' + str(k + 1)], data['SSA_' + str('{:02d}'.format(k+1)) + 'ref'])


########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''
ymax = np.zeros(2)

for k in range(2):
    data['Bmin' + str(k + 1)] = np.sqrt(np.divide(data['S_NN_noise'], data['S21_' + str(k + 1)])) * B_ref
    data['Bmin' + str(k + 1)] = np.divide(data['Bmin' + str(k + 1)],
                                          np.sqrt(np.multiply(data['SNR_' + str('{:02d}'.format(k+1))], RBW)))
    data['Bmin_min' + str(k + 1)] = data['Bmin' + str(k + 1)].min()


########################################################################################################################
'''SAVE DICTIONARY'''
pickle_out = open("sensitivity_old.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
########################################################################################################################

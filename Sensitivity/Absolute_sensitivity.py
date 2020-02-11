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
nu_ref1 = 550 * 1e3  # Func. gen. driving freq.
nu_ref2 = 150 * 1e3  # Func. gen. driving freq.
V_drive1 = math.sqrt(math.pow(10, 2.73) * 50 * math.pow(10, 0.9) * 1e-3)  # Voltage driven to the coil
V_drive2 = math.sqrt(math.pow(10, 2.73) * 50 * math.pow(10, 0.6) * 1e-3)  # Voltage driven to the coil
RBW = 30  # Resolution bandwidth
I_driven11 = V_drive1 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref1 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
# I_driven11 = I_driven12 = I_driven21 = I_driven22 = 0.473
I_driven12 = V_drive1 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref2 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref11 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven11 / radius
print(B_ref11)
B_ref12 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven12 / radius
I_driven21 = V_drive2 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref1 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
I_driven22 = V_drive2 / math.sqrt(math.pow(R, 2) + math.pow((nu_ref2 * 2 * math.pi), 2) * math.pow(L, 2))  # Coils current
B_ref21 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven21 / radius
B_ref22 = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven22 / radius

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for i in [0, 2, 5, 7, 8, 9]:
    for k in range(2):
        # with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
        #           + '\\Absolute_sensitivity_090819_FG\\SSA_' + str(i) + str(k + 1) + '.csv') as a:
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

'''Sensitivity for flux concentrator far, applying 9dBm drive with the NA'''
data['SSA_noise_550_9dBm_far'] = data['SSA_01'][370:380, 1].max()
data['SSA_noise_150_9dBm_far'] = data['SSA_01'][30:50, 1].max()
data['SSA_ref_550_9dBm_far'] = data['SSA_51'][250:430, 1].max()
data['SSA_ref_150_9dBm_far'] = data['SSA_71'][:200, 1].max()

data['SNR_550_9dBm_far'] = np.power(10, np.divide(data['SSA_ref_550_9dBm_far'] - data['SSA_noise_550_9dBm_far'], 10))
data['SNR_150_9dBm_far'] = np.power(10, np.divide(data['SSA_ref_150_9dBm_far'] - data['SSA_noise_150_9dBm_far'], 10))

data['SNN_noise_9dBm_far'] = np.power(10., np.divide(data['SSA_01'][:, 1], 10.))
data['SNN_550_9dBm_far'] = np.power(10., np.divide(data['SSA_51'][:, 1], 10.))
data['SNN_150_9dBm_far'] = np.power(10., np.divide(data['SSA_71'][:, 1], 10.))
data['SNN_noise_9dBm_far'] = np.divide(data['SNN_noise_9dBm_far'], data['SNN_noise_9dBm_far'][375])
data['SNN_550_9dBm_far'] = np.divide(data['SNN_550_9dBm_far'], data['SNN_550_9dBm_far'][375])
data['SNN_150_9dBm_far'] = np.divide(data['SNN_150_9dBm_far'], data['SNN_150_9dBm_far'][42])

'''Sensitivity for flux concentrator close, applying 9dBm drive with the NA'''
data['SSA_noise_550_9dBm_close'] = data['SSA_02'][370:380, 1].max()
data['SSA_noise_150_9dBm_close'] = data['SSA_02'][30:50, 1].max()
data['SSA_ref_550_9dBm_close'] = data['SSA_52'][250:430, 1].max()
data['SSA_ref_150_9dBm_close'] = data['SSA_72'][:200, 1].max()

data['SNR_550_9dBm_close'] = np.power(10, np.divide(data['SSA_ref_550_9dBm_close'] - data['SSA_noise_550_9dBm_close'], 10))
data['SNR_150_9dBm_close'] = np.power(10, np.divide(data['SSA_ref_150_9dBm_close'] - data['SSA_noise_150_9dBm_close'], 10))

data['SNN_noise_9dBm_close'] = np.power(10., np.divide(data['SSA_02'][:, 1], 10.))
data['SNN_550_9dBm_close'] = np.power(10., np.divide(data['SSA_52'][:, 1], 10.))
data['SNN_150_9dBm_close'] = np.power(10., np.divide(data['SSA_72'][:, 1], 10.))
data['SNN_noise_9dBm_close'] = np.divide(data['SNN_noise_9dBm_close'], data['SNN_noise_9dBm_close'][375])
data['SNN_550_9dBm_close'] = np.divide(data['SNN_550_9dBm_close'], data['SNN_550_9dBm_close'][375])
data['SNN_150_9dBm_close'] = np.divide(data['SNN_150_9dBm_close'], data['SNN_150_9dBm_close'][42])

'''Sensitivity for flux concentrator far, applying 6dBm drive with the NA'''
data['SSA_noise_550_6dBm_far'] = data['SSA_21'][370:380, 1].max()
data['SSA_noise_150_6dBm_far'] = data['SSA_21'][30:50, 1].max()
data['SSA_ref_550_6dBm_far'] = data['SSA_81'][250:430, 1].max()
data['SSA_ref_150_6dBm_far'] = data['SSA_91'][:200, 1].max()

data['SNR_550_6dBm_far'] = np.power(10, np.divide(data['SSA_ref_550_6dBm_far'] - data['SSA_noise_550_6dBm_far'], 10))
data['SNR_150_6dBm_far'] = np.power(10, np.divide(data['SSA_ref_150_6dBm_far'] - data['SSA_noise_150_6dBm_far'], 10))

data['SNN_noise_6dBm_far'] = np.power(10., np.divide(data['SSA_21'][:, 1], 10.))
data['SNN_550_6dBm_far'] = np.power(10., np.divide(data['SSA_81'][:, 1], 10.))
data['SNN_150_6dBm_far'] = np.power(10., np.divide(data['SSA_91'][:, 1], 10.))
data['SNN_noise_6dBm_far'] = np.divide(data['SNN_noise_6dBm_far'], data['SNN_noise_6dBm_far'][375])
data['SNN_550_6dBm_far'] = np.divide(data['SNN_550_6dBm_far'], data['SNN_550_6dBm_far'][375])
data['SNN_150_6dBm_far'] = np.divide(data['SNN_150_6dBm_far'], data['SNN_150_6dBm_far'][42])

'''Sensitivity for flux concentrator close, applying 9dBm drive with the NA'''
data['SSA_noise_550_6dBm_close'] = data['SSA_22'][370:380, 1].max()
data['SSA_noise_150_6dBm_close'] = data['SSA_22'][30:50, 1].max()
data['SSA_ref_550_6dBm_close'] = data['SSA_82'][250:430, 1].max()
data['SSA_ref_150_6dBm_close'] = data['SSA_92'][:200, 1].max()

data['SNR_550_6dBm_close'] = np.power(10, np.divide(data['SSA_ref_550_6dBm_close'] - data['SSA_noise_550_6dBm_close'], 10))
data['SNR_150_6dBm_close'] = np.power(10, np.divide(data['SSA_ref_150_6dBm_close'] - data['SSA_noise_150_6dBm_close'], 10))

data['SNN_noise_6dBm_close'] = np.power(10., np.divide(data['SSA_22'][:, 1], 10.))
data['SNN_550_6dBm_close'] = np.power(10., np.divide(data['SSA_82'][:, 1], 10.))
data['SNN_150_6dBm_close'] = np.power(10., np.divide(data['SSA_92'][:, 1], 10.))
data['SNN_noise_6dBm_close'] = np.divide(data['SNN_noise_6dBm_close'], data['SNN_noise_6dBm_close'][375])
data['SNN_550_6dBm_close'] = np.divide(data['SNN_550_6dBm_close'], data['SNN_550_6dBm_close'][375])
data['SNN_150_6dBm_close'] = np.divide(data['SNN_150_6dBm_close'], data['SNN_150_6dBm_close'][42])

########################################################################################################################
'''Read Network analyzer and calculate S_21 in not dB'''
for i in [0, 2]:
    for k in range(2):
        # with open('C:\\Users\\Fernando\\Documents\Phd\\9thAug'
        #           + '\\Absolute_sensitivity_090819_FG\\TRACE' + str(i) + str(k + 1) + '.csv') as a:
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\9thAug'
                  + '\\Absolute_sensitivity_090819_FG\\TRACE' + str(i) + str(k + 1) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []

            for row in df:
                df_temp.append(row)
            df = df_temp[3:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['TRACE' + str(i) + str(k + 1)] = np.reshape(np.array(df), (-1, 2))

        data['S21_' + str(i) + str(k + 1)] = np.power(10, np.divide(data['TRACE' + str(i) + str(k + 1)][:, 1], 10))

'''Sensitivity for flux concentrator far, applying 9dBm drive with the NA'''
data['S21_550_01'] = np.divide(data['S21_01'], data['S21_01'][375])
data['S21_150_01'] = np.divide(data['S21_01'], data['S21_01'][42])
data['S21_550_02'] = np.divide(data['S21_02'], data['S21_01'][375])
data['S21_150_02'] = np.divide(data['S21_02'], data['S21_01'][42])

data['S21_550_21'] = np.divide(data['S21_21'], data['S21_21'][375])
data['S21_150_21'] = np.divide(data['S21_21'], data['S21_21'][42])
data['S21_550_22'] = np.divide(data['S21_22'], data['S21_21'][375])
data['S21_150_22'] = np.divide(data['S21_22'], data['S21_21'][42])

########################################################################################################################
'''Calculate the Sensitivity in function of frequency'''

data['Bmin_550_9dBm_far'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_9dBm_far'], data['S21_550_01'])),
                                        np.divide(B_ref11, np.sqrt(np.multiply(data['SNR_550_9dBm_far'], RBW))))

data['Bmin_150_9dBm_far'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_9dBm_far'], data['S21_150_01'])),
                                        np.divide(B_ref12, np.sqrt(np.multiply(data['SNR_150_9dBm_far'], RBW))))

data['Bmin_550_9dBm_close'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_9dBm_close'], data['S21_550_02'])),
                                          np.divide(B_ref11, np.sqrt(np.multiply(data['SNR_550_9dBm_close'], RBW))))

data['Bmin_150_9dBm_close'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_9dBm_close'], data['S21_150_02'])),
                                          np.divide(B_ref12, np.sqrt(np.multiply(data['SNR_150_9dBm_close'], RBW))))

data['Bmin_550_6dBm_far'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_6dBm_far'], data['S21_550_21'])),
                                        np.divide(B_ref21, np.sqrt(np.multiply(data['SNR_550_6dBm_far'], RBW))))

data['Bmin_150_6dBm_far'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_6dBm_far'], data['S21_150_21'])),
                                        np.divide(B_ref22, np.sqrt(np.multiply(data['SNR_150_6dBm_far'], RBW))))

data['Bmin_550_6dBm_close'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_6dBm_close'], data['S21_550_22'])),
                                          np.divide(B_ref21, np.sqrt(np.multiply(data['SNR_550_9dBm_close'], RBW))))

data['Bmin_150_6dBm_close'] = np.multiply(np.sqrt(np.divide(data['SNN_noise_6dBm_close'], data['S21_150_22'])),
                                          np.divide(B_ref22, np.sqrt(np.multiply(data['SNR_150_6dBm_close'], RBW))))

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("simple_sensitivity_2mm.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################

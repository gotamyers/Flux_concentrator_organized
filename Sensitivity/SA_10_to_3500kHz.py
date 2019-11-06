import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (np.log10(16 * radius / dwire) - 2)  # Inductance
frequencies = np.asarray([11, 50, 110, 300, 500, 800, 1000, 1500, 2000, 2500, 3000, 3500])
noise_frequencies = [500, 1000, 1500, 2000, 2500, 3000, 3500]
# nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive1 = 10/(2*math.sqrt(2))  # Voltagem driven to the coil
V_drive2 = 5/(2*math.sqrt(2))  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven1 = np.divide(V_drive1, np.sqrt(R**2 + (1000*frequencies * 2 * np.pi)**2*L**2))  # Coils current
I_driven2 = np.divide(V_drive2, np.sqrt(R**2 + (1000*frequencies * 2 * np.pi)**2*L**2))
B_ref1 = pow(4.5, 1.5) * mu0 * Ncoils * I_driven1 / radius
B_ref2 = pow(4.5, 1.5) * mu0 * Ncoils * I_driven1 / radius

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for k in noise_frequencies:
    for p in [5, 10]:
        # with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\6thNov'
                  + '\\SSA_'+str(p)+'n' + str(k) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['noise'+str(p) + str(k)] = np.reshape(np.array(df), (-1, 2))
        data['noise'+str(p) + str(k)] = np.array(df)
        data['noiseV'+str(p) + str(k)] = np.power(10, data['noise'+str(p) + str(k)][:, 1]/10)

for k in frequencies:
    for p in [5, 10]:
    # with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\6thNov'
                  + '\\SSA_'+str(p) + 'a' + str(k) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_'+str(p) + 'a' + str(k)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_'+str(p) + 'a' + str(k)] = np.array(df)
        driven_freq = np.where((data['SSA_'+str(p) + 'a' + str(k)][:, 0] > (k - 1)*1000) &
                               (data['SSA_'+str(p) + 'a' + str(k)][:, 0] < (k + 1)*1000))
        data['signal'+str(p) + 'a' + str(k)] = data['SSA_'+str(p) + 'a' + str(k)][driven_freq, 1].max()
        if k < 1000:
            data['noise_max'+str(p) + 'a' + str(k)] = data['noise'+str(p)+'500'][driven_freq, 1].max()
        else:
            data['noise_max' + str(p) + 'a' + str(k)] = data['noise'+str(p)+str(k)][driven_freq, 1].max()

        data['signalV'+str(p) + 'a' + str(k)] = np.power(10, data['signal'+str(p) + 'a' + str(k)]/10)
        data['noise_maxV'+str(p) + 'a' + str(k)] = np.power(10, data['noise_max'+str(p) + 'a' + str(k)]/10)
        data['SNRV'+str(p) + 'a' + str(k)] = (data['signalV'+str(p) + 'a' + str(k)] - data['noise_maxV'+str(p) + 'a' + str(k)])/data['noise_maxV'+str(p) + 'a' + str(k)]

        data['SNR'+str(p) + 'a' + str(k)] = data['signal'+str(p) + 'a' + str(k)] - data['noise_max'+str(p) + 'a' + str(k)]
        # data['S_NN' + str(i+1) + 'a' + str(k)] = np.power(10, np.divide(data['noise500'][:, 1], 10))
        ind_freq = np.where(frequencies == k)
        if data['SNRV'+str(p) + 'a' + str(k)]*RBW <= 0:
            data['SNRV'+str(p) + 'a' + str(k)] = 0
            data['SensitivityV'+str(p) + 'a' + str(k)] = 0
        else:
            data['SensitivityV'+str(p) + 'a' + str(k)] = np.divide(B_ref1[ind_freq], np.sqrt(data['SNRV'+str(p) +'a' + str(k)]*RBW))

        if data['SNR'+str(p) + 'a' + str(k)]*RBW <= 0:
            data['Sensitivity'+str(p) + 'a' + str(k)] = 0
        else:
            data['Sensitivity'+str(p) + 'a' + str(k)] = np.divide(B_ref1[ind_freq], np.sqrt(data['SNR'+str(p) + 'a' + str(k)]*RBW))
        # print(B_ref[ind_freq])
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\6thNov'
                  + '\\SSA_'+str(p) + 'b' + str(k) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_'+str(p) + 'b' + str(k)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_'+str(p) + 'b' + str(k)] = np.array(df)
        driven_freq = np.where((data['SSA_'+str(p) + 'b' + str(k)][:, 0] > (k - 1)*1000) &
                               (data['SSA_'+str(p) + 'b' + str(k)][:, 0] < (k + 1)*1000))
        data['signal'+str(p) + 'b' + str(k)] = data['SSA_'+str(p) + 'b' + str(k)][driven_freq, 1].max()
        if k < 1000:
            data['noise_max'+str(p) + 'b' + str(k)] = data['noise'+str(p)+'500'][driven_freq, 1].max()
        else:
            data['noise_max' + str(p) + 'b' + str(k)] = data['noise'+str(p)+str(k)][driven_freq, 1].max()

        data['signalV'+str(p) + 'b' + str(k)] = np.power(10, data['signal'+str(p) + 'b' + str(k)]/10)
        data['noise_maxV'+str(p) + 'b' + str(k)] = np.power(10, data['noise_max'+str(p) + 'b' + str(k)]/10)
        data['SNRV'+str(p) + 'b' + str(k)] = (data['signalV'+str(p) + 'b' + str(k)] - data['noise_maxV'+str(p) + 'b' + str(k)])/data['noise_maxV'+str(p) + 'b' + str(k)]

        data['SNR'+str(p) + 'b' + str(k)] = data['signal'+str(p) + 'b' + str(k)] - data['noise_max'+str(p) + 'b' + str(k)]
        # data['S_NN' + str(i+1) + 'a' + str(k)] = np.power(10, np.divide(data['noise500'][:, 1], 10))
        ind_freq = np.where(frequencies == k)
        if data['SNRV'+str(p) + 'b' + str(k)]*RBW <= 0:
            data['SNRV'+str(p) + 'b' + str(k)] = 0
            data['SensitivityV'+str(p) + 'b' + str(k)] = 0
        else:
            data['SensitivityV'+str(p) + 'b' + str(k)] = np.divide(B_ref1[ind_freq], np.sqrt(data['SNRV'+str(p) +'b' + str(k)]*RBW))

        if data['SNR'+str(p) + 'b' + str(k)]*RBW <= 0:
            data['Sensitivity'+str(p) + 'b' + str(k)] = 0
        else:
            data['Sensitivity'+str(p) + 'b' + str(k)] = np.divide(B_ref1[ind_freq], np.sqrt(data['SNR'+str(p) + 'b' + str(k)]*RBW))

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("2mmflux_SA_funcgen_10to1000khz.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Plot signal'''
# signal_far = np.zeros(len(frequencies))
# signal_close = np.zeros(len(frequencies))
# sensitivity_far = np.zeros(len(frequencies))
# sensitivity_close = np.zeros(len(frequencies))
# noise_maxV = np.zeros(len(frequencies))
# for i in range(len(frequencies)):
#     signal_far[i] = data['signalV1a' + str(frequencies[i])]
#     signal_close[i] = data['signalV2a' + str(frequencies[i])]
#     sensitivity_far[i] = data['SensitivityV1a' + str(frequencies[i])]
#     sensitivity_close[i] = data['SensitivityV2a' + str(frequencies[i])]
#     noise_maxV[i] = data['noise_maxV1a' + str(frequencies[i])]
# plt.figure(1)
# for k in frequencies:
# plt.scatter(frequencies, 10*np.log10(signal_far), label='far', color='firebrick')
# plt.scatter(frequencies, 10*np.log10(signal_close), label='close', color='k')
# plt.plot(1e-3*data['noise500'][:, 0], 10*np.log10(data['noiseV500']), label='noise', color='cornflowerblue', linewidth=0.5, linestyle='--')
# plt.scatter(frequencies, 10*np.log10(noise_maxV))
# plt.xlim(9, 1000)
# # plt.ylim(0., 2.e-6)
# plt.ylim(-110, -50)
# plt.xscale('log')
# # plt.yscale('log')
# plt.legend(loc='upper right')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Power (dB)')
# plt.title('Spectrum analyser signal')
#
# plt.figure(2)
#
# plt.scatter(frequencies, 1e9*sensitivity_far, label='far', color='firebrick')
# plt.scatter(frequencies, 1e9*sensitivity_close, label='close', color='k')
#
# plt.xscale('log')
# plt.yscale('log')
# plt.legend(loc='lower left')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Sensitivity nT')
# plt.title('Sensitivity')
#
# plt.show()




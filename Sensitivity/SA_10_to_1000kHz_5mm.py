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
frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 990])
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]
# nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = 10/(2*math.sqrt(2))  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = np.divide(V_drive, np.sqrt(R**2 + (1000*frequencies * 2 * np.pi)**2*L**2))  # Coils current
B_ref = pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius
letters = ['a', 'b', 'c']

########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\13thNov'
          + '\\SSA_n500.csv') as a:

    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['noise'] = np.reshape(np.array(df), (-1, 2))
data['noise'] = np.array(df)
data['noiseV'] = np.power(10, data['noise'][:, 1]/10)

for k in frequencies:
    for i in letters:
        # with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\13thNov'
                  + '\\SSA_' + i + str(k) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + i + str(k)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + i + str(k)] = np.array(df)
        driven_freq = np.where((data['SSA_' + i + str(k)][:, 0] > (k - 1)*1000) &
                               (data['SSA_' + i + str(k)][:, 0] < (k + 1)*1000))
        data['signal' + i + str(k)] = data['SSA_' + i + str(k)][driven_freq, 1].max()
        data['noise_max' + str(k)] = data['noise'][driven_freq, 1].max()

        data['signalV' + i + str(k)] = np.power(10, data['signal' + i + str(k)]/10)
        data['noise_maxV' + str(k)] = np.power(10, data['noise_max' + str(k)]/10)
        data['SNRV' + i + str(k)] = (data['signalV' + i + str(k)] - data['noise_maxV' + str(k)])/data['noise_maxV' + str(k)]

        data['SNR' + i + str(k)] = data['signal' + i + str(k)] - data['noise_max' + str(k)]
        # data['S_NN' + str(i+1) + 'a' + str(k)] = np.power(10, np.divide(data['noise500'][:, 1], 10))
        ind_freq = np.where(frequencies == k)
        if data['SNRV' + i + str(k)]*RBW <= 0:
            data['SNRV' + i + str(k)] = 0
            data['SensitivityV' + i + str(k)] = 0
        else:
            data['SensitivityV' + i + str(k)] = np.divide(B_ref[ind_freq], np.sqrt(data['SNRV' + i + str(k)] * RBW))

        if data['SNR' + i + str(k)]*RBW <= 0:
            data['Sensitivity' + i + str(k)] = 0
        else:
            data['Sensitivity' + i + str(k)] = np.divide(B_ref[ind_freq], np.sqrt(data['SNR' + i + str(k)]*RBW))

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("2and5mmflux_SA_funcgen_10to1000khz.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Plot signal'''
signal_far = np.zeros(len(frequencies))
signal_close2mm = np.zeros(len(frequencies))
signal_close5mm = np.zeros(len(frequencies))
SNR_far = np.zeros(len(frequencies))
SNR_close = np.zeros(len(frequencies))
# sensitivity_far = np.zeros(len(frequencies))
# sensitivity_close = np.zeros(len(frequencies))
# noise_maxV = np.zeros(len(frequencies))
enhance_factor2mm = np.zeros(len(frequencies))
enhance_factor5mm = np.zeros(len(frequencies))
enhance_factor5to2 = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    signal_far[i] = data['signalVa' + str(frequencies[i])]
    signal_close2mm[i] = data['signalVb' + str(frequencies[i])]
    signal_close5mm[i] = data['signalVc' + str(frequencies[i])]
    if data['signalVa' + str(frequencies[i])]<=data['noise_maxV' + str(frequencies[i])]:
        SNR_far[i] = data['noise_maxV' + str(frequencies[i])]
    else:
        SNR_far[i] = data['signalVa' + str(frequencies[i])] - data['noise_maxV' + str(frequencies[i])]
#     sensitivity_far[i] = data['SensitivityV1a' + str(frequencies[i])]
#     sensitivity_close[i] = data['SensitivityV2a' + str(frequencies[i])]
#     noise_maxV[i] = data['noise_maxV1a' + str(frequencies[i])]
    enhance_factor2mm[i] = (data['signalVb' + str(frequencies[i])] - data['noise_maxV' + str(frequencies[i])])/(SNR_far[i])
    enhance_factor5mm[i] = (data['signalVc' + str(frequencies[i])] - data['noise_maxV' + str(frequencies[i])])/(SNR_far[i])
    enhance_factor5to2[i] = (data['signalVc' + str(frequencies[i])] - data['noise_maxV' + str(frequencies[i])])/(data['signalVb' + str(frequencies[i])] - data['noise_maxV' + str(frequencies[i])])

plt.figure(1)
plt.scatter(frequencies, 10*np.log10(signal_far), label='far', color='firebrick')
plt.scatter(frequencies, 10*np.log10(signal_close2mm), label='close', color='k')
plt.scatter(frequencies, 10*np.log10(signal_close5mm), label='close', color='green')
plt.plot(1e-3*data['noise'][:, 0], 10*np.log10(data['noiseV']), label='noise', color='cornflowerblue', linewidth=0.5, linestyle='--')
# plt.scatter(frequencies, 10*np.log10(noise_maxV))
# plt.xlim(9, 1000)
# # plt.ylim(0., 2.e-6)
# plt.ylim(-110, -50)
plt.xscale('log')
# # plt.yscale('log')
# plt.legend(loc='upper right')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Power (dB)')
# plt.title('Spectrum analyser signal')
#
plt.figure(2)
#
plt.scatter(frequencies, 10*np.log10(enhance_factor2mm), label='2mm', color='black')
plt.scatter(frequencies, 10*np.log10(enhance_factor5mm), label='5mm', color='green')
plt.scatter(frequencies, 10*np.log10(enhance_factor5to2), label='5 to 2', color='firebrick')
#
plt.xscale('log')
# plt.yscale('log')
# plt.legend(loc='lower left')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Sensitivity nT')
# plt.title('Sensitivity')
#
plt.show()

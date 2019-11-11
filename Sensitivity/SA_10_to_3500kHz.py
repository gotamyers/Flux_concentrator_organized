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

all_noise = data['noise5500'][:, 1]
frequency_range = data['noise5500'][:, 0]
for k in noise_frequencies[1:]:
    frequency_range = np.append(frequency_range, data['noise5' + str(k)][:, 0])
    all_noise = np.append(all_noise, data['noise5' + str(k)][:, 1])

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
            data['SensitivityV'+str(p) + 'b' + str(k)] = np.divide(B_ref2[ind_freq], np.sqrt(data['SNRV'+str(p) +'b' + str(k)]*RBW))

        if data['SNR'+str(p) + 'b' + str(k)]*RBW <= 0:
            data['Sensitivity'+str(p) + 'b' + str(k)] = 0
        else:
            data['Sensitivity'+str(p) + 'b' + str(k)] = np.divide(B_ref2[ind_freq], np.sqrt(data['SNR'+str(p) + 'b' + str(k)]*RBW))

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("2mmflux_SA_funcgen_10to1000khz.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Make things plottable'''
signal_far1 = np.zeros(len(frequencies))
signal_close1 = np.zeros(len(frequencies))
signal_far2 = np.zeros(len(frequencies))
signal_close2 = np.zeros(len(frequencies))
# sensitivity_far = np.zeros(len(frequencies))
# sensitivity_close = np.zeros(len(frequencies))
noise_max5Va = np.zeros(len(frequencies))
noise_max10Va = np.zeros(len(frequencies))
noise_max5Vb = np.zeros(len(frequencies))
noise_max10Vb = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    signal_far1[i] = data['signalV5a' + str(frequencies[i])]
    signal_close1[i] = data['signalV5b' + str(frequencies[i])]
    signal_far2[i] = data['signalV10a' + str(frequencies[i])]
    signal_close2[i] = data['signalV10b' + str(frequencies[i])]
#     sensitivity_far[i] = data['SensitivityV1a' + str(frequencies[i])]
#     sensitivity_close[i] = data['SensitivityV2a' + str(frequencies[i])]
    noise_max5Va[i] = data['noise_maxV5a' + str(frequencies[i])]
    noise_max10Va[i] = data['noise_maxV10a' + str(frequencies[i])]
    noise_max5Vb[i] = data['noise_maxV5b' + str(frequencies[i])]
    noise_max10Vb[i] = data['noise_maxV10b' + str(frequencies[i])]
enhanc_factor1 = (signal_close1 - noise_max5Va)/(signal_far1)
enhanc_factor2 = (signal_close2 - noise_max10Va)/(signal_far2)
exclude_ind = np.where(enhanc_factor1 <=1)
enhanc_factor1_del = np.delete(enhanc_factor1, exclude_ind, axis=0)
enhanc_factor2_del = np.delete(enhanc_factor2, exclude_ind, axis=0)
frequencies_del = np.delete(frequencies, exclude_ind, axis=0)

'''Normalize by the B field'''
B1 = np.delete(B_ref1/B_ref1[0], exclude_ind, axis=0)
B2 = np.delete(B_ref2/B_ref2[0], exclude_ind, axis=0)
########################################################################################################################
'''Plot signal'''
plt.figure(1)
# for k in frequencies:
plt.scatter(1e3*frequencies, 10*np.log10(signal_far1), label='far5', color='firebrick')
plt.scatter(1e3*frequencies, 10*np.log10(signal_close1), label='close5', color='royalblue')
plt.scatter(1e3*frequencies, 10*np.log10(signal_far2), label='far10', color='red')
plt.scatter(1e3*frequencies, 10*np.log10(signal_close2), label='close10', color='blue')
# plt.plot(1e3*frequencies, 10*np.log10(noise_max5Va), label='noise5V', color='k')
# plt.plot(1e3*frequencies, 10*np.log10(noise_max10Va), label='noise10V', color='gray')
plt.plot(frequency_range, all_noise)
# plt.plot(1e-3*data['noise500'][:, 0], 10*np.log10(data['noiseV500']), label='noise', color='cornflowerblue', linewidth=0.5, linestyle='--')
# plt.scatter(frequencies, 10*np.log10(noise_maxV))
plt.xlim(1e4, 1e7)
# # plt.ylim(0., 2.e-6)
# plt.ylim(-110, -50)
plt.xscale('log')
# # plt.yscale('log')
plt.legend(loc='upper right')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Power (dB)')
# plt.title('Spectrum analyser signal')
#
plt.figure(2)
plt.scatter(1e3*frequencies_del, 10*np.log10(enhanc_factor1_del), label='5', color='red')
plt.scatter(1e3*frequencies_del, 10*np.log10(enhanc_factor2_del), label='10', color='k')
# plt.scatter(frequencies, 1e9*sensitivity_far, label='far', color='firebrick')
# plt.scatter(frequencies, 1e9*sensitivity_close, label='close', color='k')
#
plt.xscale('log')
plt.ylim(0, 30)
# plt.yscale('log')
# plt.legend(loc='lower left')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Sensitivity nT')
# plt.title('Sensitivity')
plt.figure(3)
# plt.scatter(1e3*frequencies_del, 10*np.log10(enhanc_factor1_del/B1), label='5', color='red')
# plt.scatter(1e3*frequencies_del, 10*np.log10(enhanc_factor2_del/B2), label='5', color='k')
plt.scatter(1e3*frequencies_del, B1)
plt.xscale('log')
# plt.ylim(0, 30)

plt.show()


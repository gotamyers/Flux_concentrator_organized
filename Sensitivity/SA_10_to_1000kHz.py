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
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990])
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]
# nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = 10/(2*math.sqrt(2))  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = np.divide(V_drive, np.sqrt(R**2) + ((frequencies * 2 * np.pi)**2) * L**2)  # Coils current
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius


########################################################################################################################
'''Read Spectrum analyzer, find SNR and calculate S_NN in not dB'''
for k in noise_frequencies:
    with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
    # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\10thOct'
              + '\\SSA_n' + str(k) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['noise' + str(k)] = np.reshape(np.array(df), (-1, 2))
    data['noise' + str(k)] = np.array(df)

for k in frequencies:
    for i in range(2):
        with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
        # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\10thOct'
                  + '\\SSA_' + str(i + 1) + 'a' + str(k) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(i + 1) + 'a' + str(k)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + str(i + 1) + 'a' + str(k)] = np.array(df)
        driven_freq = np.where((data['SSA_' + str(i + 1) + 'a' + str(k)][:, 0] > (k - 1)*1000) &
                               (data['SSA_' + str(i + 1) + 'a' + str(k)][:, 0] < (k + 1)*1000))
        data['signal' + str(i + 1) + 'a' + str(k)] = data['SSA_' + str(i + 1) + 'a' + str(k)][driven_freq, 1].max()
        noise_max = data['noise500'][driven_freq, 1].max()

        data['SNR' + str(i + 1) + 'a' + str(k)] = data['signal' + str(i + 1) + 'a' + str(k)] - noise_max
        # data['S_NN' + str(i+1) + 'a' + str(k)] = np.power(10, np.divide(data['noise500'][:, 1], 10))
        ind_freq = np.where(frequencies == k)
        if data['SNR' + str(i + 1) + 'a' + str(k)]*RBW <= 0:
            data['Sensitivity' + str(i + 1) + 'a' + str(k)] = 0
        else:
            data['Sensitivity' + str(i + 1) + 'a' + str(k)] = np.divide(B_ref[ind_freq], np.sqrt(data['SNR' + str(i + 1) +
                                                                                                  'a' + str(k)]*RBW))
        # print(data['Sensitivity' + str(i + 1) + 'a' + str(k)])

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("2mmflux_SA_funcgen_10to1000khz.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Plot signal'''
signal_far = np.zeros(len(frequencies))
signal_close = np.zeros(len(frequencies))
sensitivity_far = np.zeros(len(frequencies))
sensitivity_close = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    signal_far[i] = data['signal1a' + str(frequencies[i])]
    signal_close[i] = data['signal2a' + str(frequencies[i])]
    sensitivity_far[i] = data['Sensitivity1a' + str(frequencies[i])]
    sensitivity_close[i] = data['Sensitivity2a' + str(frequencies[i])]
plt.figure(1)
# for k in frequencies:
plt.scatter(frequencies, signal_far, label='far', color='firebrick')
plt.scatter(frequencies, signal_close, label='close', color='k')
plt.plot(1e-3*data['noise500'][:, 0], data['noise500'][:, 1], label='noise', color='cornflowerblue', linewidth=0.5, linestyle='--')
plt.xlim(9, 1000)
# plt.ylim(0.00001, 0.002)
plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='lower left')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Power (dB)')
plt.title('Spectrum analyser signal')

plt.figure(2)

plt.scatter(frequencies, 1e9*sensitivity_far, label='far', color='firebrick')
plt.scatter(frequencies, 1e9*sensitivity_close, label='close', color='k')

plt.xscale('log')
plt.yscale('log')
plt.legend(loc='lower left')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Sensitivity nT')
plt.title('Sensitivity')

plt.show()




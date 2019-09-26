import csv
import math
import numpy as np
import pickle
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

data = {}

'''Calculating helmholtz coil magnetic field'''
mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
nu_ref = 550 * 1e3  # Func. gen. driving freq.
V_drive = 10/(2*math.sqrt(2)) # Voltage applied to the coil in root mean square
tal = 4
RBW = 2*math.sqrt(6)/tal  # Resolution bandwidth
I_driven = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref * 2 * math.pi), 2) * math.pow(L, 2))
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius
freq_order = 100 #mininum frequency on a particular range
########################################################################################################################
'''Read Oscilloscope'''
for i in range(10):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\20thSep'
              + '\\100_to_1000_Hz\\2_' + str((i + 1)*freq_order) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[21:-1]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]
    data['flux_far' + str(i + 1)] = np.asarray(df)

for i in range(5):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\20thSep'
              + '\\100_to_1000_Hz\\n' + str(i) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[21:-1]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]
    data['noise' + str(i)] = np.asarray(df)

'''Start fourier transform (https://www.youtube.com/watch?v=su9YSmwZmPg)'''
# n = len(df[:, 0])
# delta_t = df[1, 0] - df[0, 0]
#
# # omega = 2.0 * np.pi /delta_t
#
# fft_vals = fft(df[:, 1])
# fft_theoretical = 2.0 * np.abs(fft_vals / n)
# freqs = fftfreq(n)
# mask = freqs > 0
#
# plt.figure()
# plt.plot(freqs[mask], fft_theoretical[mask])

'''Another fourier transform (https://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python)'''

N = len(data['noise4'][:, 0])
delta_t = data['noise4'][1, 0] - data['noise4'][0, 0]

data['freq'] = np.fft.fftfreq(N, delta_t)
mask = data['freq'] > 0

data['FFT_noise4'] = np.fft.fft(data['noise4'][:, 1])
data['FFT_noise4_theoretical'] = 2.0*np.abs(data['FFT_noise4'] / N)

for i in range(10):
    data['FFT_flux_far' + str(i + 1)] = np.fft.fft(data['flux_far' + str(i + 1)][:, 1])
    data['FFT_flux_far' + str(i + 1) + '_theoretical'] = 2.0*np.abs(data['FFT_flux_far' + str(i + 1)] / N)

    driven_freq = np.where((data['freq'] > ((i+1) - 0.1)*freq_order) & (data['freq'] < ((i+1) + 0.1)*freq_order))
    # print(driven_freq)

    signal = data['FFT_flux_far' + str(i + 1) + '_theoretical'] - data['FFT_noise4_theoretical']
    flux_max = signal[driven_freq].max()
    noise_max = data['FFT_noise4_theoretical'][driven_freq].max()

    data['SNR' + str(i+1)] = flux_max/noise_max

    data['Bmin' + str(i+1)] = B_ref/(np.sqrt((data['SNR' + str(i+1)]*RBW)))
# print('Number os indexes is : ', len(data['FFT_550_coupled_theoretical']))
    print('Sensitivity is: ', data['Bmin' + str(i+1)])
# print('Noise is: ', noise_max)
# print('Signal is: ', coupled_max)

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("2mmflux_far_1to10Hz.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################

# for i in range(10):
#     plt.figure(i+1)
#     plt.plot(data['freq'][mask], 1e3*data['FFT_flux_far' + str(i + 1) + '_theoretical'][mask])
#     plt.xscale('log')
#     plt.yscale('log')
#     plt.xlim(1, 1000)
#     plt.ylim(0., 0.80)
#
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('mV/Hz')
#     # plt.title('20 khz - far')
#
# plt.figure(12)
# plt.plot(data['freq'][mask], 1e3*data['FFT_noise4_theoretical'][mask])
# plt.xlim(0.5, 10.5)
# plt.ylim(0, 0.80)
# # plt.yscale('log')
# # plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('mV')
# plt.title('Noise')
#
# plt.show()

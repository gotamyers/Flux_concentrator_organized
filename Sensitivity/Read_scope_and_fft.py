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
RBW = 490  # Resolution bandwidth
I_driven = V_drive / math.sqrt(math.pow(R, 2) + math.pow((nu_ref * 2 * math.pi), 2) * math.pow(L, 2))
B_ref = math.pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius

########################################################################################################################
'''Read Oscilloscope'''
# with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\16thSep'
#           + '\\01_20.csv') as a:
for i in range(10):
    with open('C:\\Users\\Fernando\\Documents\Phd\\20thSep\\1_to_10_kHz\\2_' + str(i+1) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[21:-1]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]
    data['flux_close_' + str((i+1)*1000)] = np.asarray(df)

for i in range(5):
    # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\16thSep'
    #           + '\\noise_5.csv') as a:
    with open('C:\\Users\\Fernando\\Documents\Phd\\20thSep\\1_to_10_kHz\\n' + str(i) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[21:-1]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]
    data['1000to10000hz_noise' + str(i)] = np.asarray(df)

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
N = len(data['1000to10000hz_noise4'][:, 0])
delta_t = data['1000to10000hz_noise4'][1, 0] - data['1000to10000hz_noise4'][0, 0]

data['freq'] = np.fft.fftfreq(N, delta_t)
mask = data['freq'] > 0

data['FFT_1000to10000hz_noise4'] = np.fft.fft(data['1000to10000hz_noise4'][:, 1])
data['FFT_1000to10000hz_noise4_theoretical'] = 2.0*np.abs(data['FFT_1000to10000hz_noise4'] / N)

for i in range(10):
    data['FFT_flux_close_' + str((i+1)*1000)] = np.fft.fft(data['flux_close_' + str((i+1)*1000)][:, 1])
    data['FFT_flux_close_' + str((i+1)*1000) + '_theoretical'] = 2.0*np.abs(data['FFT_flux_close_' + str((i+1)*1000)] / N)

    # driven_freq = np.where((data['freq'] > (i+1)*1000 - 10) & (data['freq'] < (i+1)*1000 + 10))
    # print(driven_freq)

    data['flux_close_max' + str(i + 1)] = data['FFT_flux_close_' + str((i+1)*1000) +
                                             '_theoretical'][(i+1)*1000 - 5:(i+1)*1000 + 5].max()
    data['noise_max ' + str(i+1)] = data['FFT_1000to10000hz_noise4_theoretical'][(i+1)*1000 - 5:(i+1)*1000 + 5].max()

    data['SNR' + str(i+1)] = data['flux_close_max' + str(i + 1)]/data['noise_max '+ str(i+1)]

    data['Bmin' + str(i)] = B_ref/(np.sqrt((data['SNR' + str(i+1)]*RBW)))
# # print('Number os indexes is : ', len(data['FFT_550_coupled_theoretical']))
    print('Sensitivity is: ', data['Bmin' + str(i)])
# print('Noise is: ', noise_max)
# print('Signal is: ', coupled_max)

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("scope_2mm_160919.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################

for i in range(10):
    plt.figure(i)
    plt.plot(data['freq'][mask], 1e3*data['FFT_flux_close_' + str((i+1)*1000) + '_theoretical'][mask])
    plt.xlim(990, 10010)
    plt.ylim(0, 0.70)

    plt.xlabel('Frequency (kHz)')
    plt.ylabel('SNR')
    # plt.title('20 khz - far')

plt.show()

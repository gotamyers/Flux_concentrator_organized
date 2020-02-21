import csv
import math
import numpy as np
import pickle
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

data = {}

for i in range(7):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thFeb2020'
              + '\\sc_0' + str(i) + '_1.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[3:]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['scope_0' + str(i)] = np.asarray(df)

N = len(data['scope_00'][:, 0])
delta_t = data['scope_00'][1, 0] - data['scope_00'][0, 0]

data['freq'] = np.fft.fftfreq(N, delta_t)
mask = data['freq'] > 0

data['FFT_scope_00'] = np.fft.fft(data['scope_00'][:, 1])
# data['FFT_noise4_theo'] = 20.*np.log10(np.abs(data['FFT_noise4'] / N))
data['FFT_scope_00_theo'] = (2.0*np.abs(data['FFT_scope_00'] / N))**2


for i in range(7):
    data['FFT_scope_0' + str(i)] = np.fft.fft(data['scope_0' + str(i)][:, 1])
    # data['FFT_flux_far_' + str((i+1)) + '_theo'] = 20.*np.log10(np.abs(data['FFT_flux_far_' + str((i+1))] / N))
    data['FFT_scope_0' + str(i) + '_theo'] = 2.0*(np.abs(data['FFT_scope_0' + str(i)] / N))**2
    data['dB_FFT_scope_0' + str(i) + '_theo'] = 10*np.log10(data['FFT_scope_0' + str(i) + '_theo'])



for i in range(7):
    plt.figure(i)
    plt.plot(data['freq'][mask], data['dB_FFT_scope_0' + str(i) + '_theo'][mask])
    # plt.xlim(50000, 1050000)
    # plt.ylim(-160, -60)

    plt.xlabel('Frequency (Hz)')
    # plt.ylabel('SNR')
    # plt.title('20 khz - far')

plt.show()


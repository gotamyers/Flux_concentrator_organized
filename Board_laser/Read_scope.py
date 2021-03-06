import csv
import math
import numpy as np
import pickle
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# This script is supposed to read .csv files saved with the oscilloscope, take the average of 10 measurements made for
# each attenuated power, subtract the electronical noise and plot PSD in function of frequency.

data = {}

'''Read data'''
for i in range(7):
    for k in range(5): #10 measurements with same configuration (k = 1 to 10)
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
                  + '\\Scope_' + str(i) + '_' + str(k) + '000.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row[3:])
            df = df_temp[:]
            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['scope_' + str(i) + '_' + str(k)] = np.asarray(df)


N = len(data['scope_0_0'][:, 0])
delta_t = data['scope_0_0'][1, 0] - data['scope_0_0'][0, 0]

data['freq'] = np.fft.fftfreq(N, delta_t)
mask = data['freq'] > 0

'''F.T of the amplitude'''
for i in range(7):
    for k in range(5):
        data['FFT_scope_' + str(i) + str(k)] = np.fft.fft(data['scope_' + str(i) + '_' + str(k)][:, 1])
        data['FFT_scope_' + str(i) + str(k) + '_theo'] = 2.0*(np.abs(data['FFT_scope_' + str(i) + str(k)]/N))**2
        data['dB_FFT_scope_' + str(i) + str(k) + '_theo'] = 10*np.log10(data['FFT_scope_' + str(i) + str(k) + '_theo'])

'''Averaging PSD'''
for i in range(7):
    sum = np.zeros(len(data['dB_FFT_scope_00_theo']))
    for k in range(5):
        sum = sum + data['dB_FFT_scope_' + str(i) + str(k) + '_theo']
    data['avg_dB_FFT_scope_' + str(i) + '_theo'] = sum/10



plt.figure(1)
for i in range(7):
    # plt.figure(i)
    plt.plot(data['freq'][mask], data['avg_dB_FFT_scope_' + str(i) + '_theo'][mask])
    # plt.xlim(50000, 1050000)
    # plt.ylim(-160, -60)

    plt.xlabel('Frequency (Hz)')
    # plt.ylabel('SNR')
    # plt.title('20 khz - far')

# Here, I am doing similar procedure but only for scopes noise, also averaging
for k in range(5):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
              + '\\Scope_noise_' + str(k) + '000.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[3:]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['scope_noise' + str(k)] = np.asarray(df)

for k in range(5):
    data['FFT_scope_noise' + str(k)] = np.fft.fft(data['scope_noise' + str(k)][:, 1])
    data['FFT_scope_noise' + str(k) + '_theo'] = 2.0*(np.abs(data['FFT_scope_noise' + str(k)] / N))**2
    data['dB_FFT_scope_noise' + str(k) + '_theo'] = 10*np.log10(data['FFT_scope_noise' + str(k) + '_theo'])

'''Averaging scope noise'''
sum = np.zeros(len(data['dB_FFT_scope_noise0_theo']))
for k in range(5):
    sum = sum + data['dB_FFT_scope_noise' + str(k) + '_theo']
data['avg_dB_FFT_scope_noise_theo'] = sum / 10

'''Plot test'''
plt.figure(10)
plt.plot(data['freq'][mask], data['avg_dB_FFT_scope_noise_theo'][mask])
plt.plot(data['freq'][mask], data['avg_dB_FFT_scope_0_theo'][mask])

plt.show()


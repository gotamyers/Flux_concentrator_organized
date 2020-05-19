import csv
import numpy as np
import pickle
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

data = {}

max_value = np.zeros(21)
freq_funcgen = np.asarray([1000, 500, 200, 100, 70, 50, 40, 30, 25, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2])

'''Read data'''
for i in range(21):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\29thApr2020'
              + '\\Low_pass0' + str("{:02d}".format(i)) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row[3:])
        df = df_temp[:]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['low_pass' + str(i)] = np.asarray(df)

    N = len(data['low_pass' + str(i)][:, 0])
    delta_t = data['low_pass' + str(i)][1, 0] - data['low_pass' + str(i)][0, 0]

    data['freq' + str(i)] = np.fft.fftfreq(N, delta_t)
    mask = data['freq' + str(i)] > 0

    data['FFT_low_pass' + str(i)] = np.fft.fft(data['low_pass' + str(i)][:, 1])
    data['FFT_low_pass' + str(i) + '_theo'] = 2.0*(np.abs(data['FFT_low_pass' + str(i)]/np.sqrt(N)))**2

    max_value[i] = np.amax(data['FFT_low_pass' + str(i) + '_theo'])

    # plt.figure(i)
    # plt.plot(data['freq' + str(i)][mask], data['FFT_low_pass' + str(i) + '_theo'][mask])
    # plt.xlim(0, 50)

plt.figure(1)
plt.scatter(freq_funcgen, max_value[:-1])

plt.xscale('log')
plt.yscale('log')



plt.show()

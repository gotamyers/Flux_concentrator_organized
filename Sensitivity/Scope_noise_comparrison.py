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
for i in range(5):
    # with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\19thSep'
    #           + '\\noise' + str(i) + '.csv') as a:
    with open('C:\\Users\\Fernando\\Documents\Phd\\20thSep\\100_to_1000_Hz\\n' + str(i) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[21:-1]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]
    data['noise' + str(i)] = np.asarray(df)


'''Take the fourier transform'''
for i in range(5):
    N = len(data['noise' + str(i)][:, 0])
    delta_t = data['noise' + str(i)][1, 0] - data['noise' + str(i)][0, 0]

    data['freq' + str(i)] = np.fft.fftfreq(N, delta_t)
    mask = data['freq' + str(i)] > 0
    data['freq' + str(i)] = data['freq' + str(i)][mask]

    data['FFT_noise' + str(i)] = np.fft.fft(data['noise' + str(i)][:, 1])
    data['FFT_noise' + str(i) + '_theoretical'] = 2.0*np.abs(data['FFT_noise' + str(i)] / N)
    data['FFT_noise' + str(i) + '_theoretical'] = data['FFT_noise' + str(i) + '_theoretical'][mask]

    # driven_freq = np.where((data['freq' + str(i)] < 25000) & (data['freq'] > 15000))
    # print(driven_freq)

# coupled_max = data['FFT_550_coupled_theoretical'][31:50].max()
# noise_max = data['FFT_550_noise_theoretical'][31:50].max()

# SNR = coupled_max/noise_max

# B = B_ref/(np.sqrt((SNR*RBW)))
# print('Number os indexes is : ', len(data['FFT_550_coupled_theoretical']))
# print('Sensitivity is: ', B)
# print('Noise is: ', noise_max)
# print('Signal is: ', coupled_max)

########################################################################################################################
'''SAVE DICTIONARY'''
pickle_out = open("2mmflux_scope_noise_100to1000hz.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
########################################################################################################################

for i in range(5):
    plt.figure(i)

    plt.plot(data['freq' + str(i)], data['FFT_noise' + str(i) + '_theoretical'])

    plt.title('Noise' + str(i))
    plt.xlim(0, 10000)
    plt.ylim(0, 0.00040)
    # plt.legend(loc='upper right')

plt.show()

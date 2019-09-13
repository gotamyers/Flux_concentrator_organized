import csv
import scipy.fftpack
import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

data = {}

'''Calculating helmholtz coil magnetic field'''
# mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
# Ncoils = 10  # Number of turns
# dwire = 0.8  # Wires thickness
# radius = 0.03  # Coil radius
# R = 50  # Resistance (ohms)
# L = 2 * mu0 * radius * Ncoils * (math.log10(16 * radius / dwire) - 2)  # Inductance
# RBW = 30  # Resolution bandwidth
# V_drive = 1.78  # Voltage driven to the coil


########################################################################################################################
'''Read Oscilloscope'''
with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thSep'
          + '\\1200khz_sine.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[21:-1]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]
df = np.asarray(df)

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
N = len(df[:, 0])
delta_t = df[1, 0] - df[0, 0]

Y = np.fft.fft(df[:, 1])
Y_theoretical = 2.0*np.abs(Y / N)
freq = np.fft.fftfreq(N, delta_t)
mask = freq > 0

plt.figure()
plt.plot(freq[mask], np.abs(Y_theoretical[mask]))


plt.show()

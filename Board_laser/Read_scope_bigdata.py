import csv
import math
import numpy as np
import pickle
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# This script is supposed to read .csv files saved with the oscilloscope, and save as a dictionary so that later,
# a Fourier Transform can be done.

data = {}

# for i in range(8):
#     '''Read data'''
#     for k in range(5): #5 measurements with same configuration (k = 0 to 4)
#         with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
#                   + '\\Scope_' + str(i) + '_' + str(k) + '000.csv') as a:
#
#             df = csv.reader(a, delimiter=',')
#             df_temp = []
#             for row in df:
#                 df_temp.append(row[3:])
#             df = df_temp[:]
#             for j in range(len(df)):
#                 df[j] = [np.float(df[j][0]), np.float(df[j][1])]
#
#         data['scope_' + str(k)] = np.asarray(df)
#
#     ####################################################################################################################
#     '''SAVE DICTIONARY'''
#     pickle_out = open("scope_" + str(i) + ".pickle", "wb")
#     pickle.dump(data, pickle_out)
#     pickle_out.close()
#     ####################################################################################################################

# Here, going to do only once for the scope's noise alone

# data_plot = {}
# n_avg = 5      # number of averages
# '''Read data'''
# for k in range(5): #5 measurements with same configuration (k = 0 to 4)
#     with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
#               + '\\Scope_noise' + str(k) + '000.csv') as a:
#
#         df = csv.reader(a, delimiter=',')
#         df_temp = []
#         for row in df:
#             df_temp.append(row[3:])
#         df = df_temp[:]
#         for j in range(len(df)):
#             df[j] = [np.float(df[j][0]), np.float(df[j][1])]
#
#     data['scope_noise' + str(k)] = np.asarray(df)
#
# N = len(data['scope_noise0'][:, 0])
# delta_t = data['scope_noise0'][1, 0] - data['scope_noise0'][0, 0]
#
# data['freq'] = np.fft.fftfreq(N, delta_t)
# mask = data['freq'] > 0
#
#
# '''F.T of the amplitude'''
# for k in range(5):
#     data['FFT_scope_noise' + str(k)] = np.fft.fft(data['scope_noise' + str(k)][:, 1])
#     data['FFT_scope_noise' + str(k) + '_theo'] = 2.0*(np.abs(data['FFT_scope_noise' + str(k)]/N))**2
#
#
# '''Averaging PSD'''
# soma = np.zeros(len(data['FFT_scope_noise0_theo']))
# for k in range(5):
#     soma = soma + data['FFT_scope_noise' + str(k) + '_theo']
# data['avg_FFT_scope_noise_theo'] = soma/n_avg
#
# data_plot['dB_avg_FFT_scope_noise_theo'] = 10 * np.log10(data['avg_FFT_scope_noise_theo'])
# data_plot['freq'] = data['freq']
#
# ########################################################################################################################
# '''SAVE DICTIONARY'''
# pickle_out = open("dB_avg_FFT_noise.pickle", "wb")
# pickle.dump(data_plot, pickle_out)
# pickle_out.close()
# ########################################################################################################################

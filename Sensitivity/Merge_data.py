import numpy as np
import pickle
import math
import matplotlib.pyplot as plt

data_mergeFFT = {}

pickle_in = open("2mmflux_close_1to10Hz.pickle", "rb")
data_close_1to10Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_1to10Hz.pickle", "rb")
data_far_1to10Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_close_10to100Hz.pickle", "rb")
data_close_10to100Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_10to100Hz.pickle", "rb")
data_far_10to100Hz = pickle.load(pickle_in)

data_mergeFFT['flux_far1to10'] = []
data_mergeFFT['flux_close1to10'] = []
data_mergeFFT['flux_far10to100'] = []
data_mergeFFT['flux_close10to100'] = []

'''Plot graph'''
plt.figure(1)
for i in range(10):
    driven_freq = np.where((data_far_1to10Hz['freq'] >= (i + 1) * 1 - 0.5) &
                           (data_far_1to10Hz['freq'] < (i + 1) * 1 + 0.5))
#
#     data_mergeFFT['flux_far1to10'] = np.append(data_mergeFFT['flux_far1to10'], data_far_1to10Hz['FFT_flux_far_' + str(i + 1) +
#                                                                                       '_theo'][driven_freq])
#     data_mergeFFT['flux_close1to10'] = np.append(data_mergeFFT['flux_close1to10'],
#                                             data_close_1to10Hz['FFT_flux_close_' + str(i + 1) + '_theo'][driven_freq])
#
#     data_mergeFFT['flux_far10to100'] = np.append(data_mergeFFT['flux_far10to100'],
#                                           data_far_10to100Hz['FFT_flux_far_' + str(i + 1) + '_theo'][driven_freq2])
#     data_mergeFFT['flux_close10to100'] = np.append(data_mergeFFT['flux_close10to100'],
#                                             data_close_10to100Hz['FFT_flux_close_' + str(i + 1) + '_theo'][driven_freq2])
#
# driven_freq = np.where((data_far_1to10Hz['freq'] > 0.5) & (data_far_1to10Hz['freq'] < 10.5))
# data_mergeFFT['freq_1to10Hz'] = data_far_1to10Hz['freq'][driven_freq]
#
# driven_freq2 = np.where((data_far_10to100Hz['freq'] > 9.5) & (data_far_10to100Hz['freq'] < 100.5))
# data_mergeFFT['freq_10to100Hz'] = data_far_10to100Hz['freq'][driven_freq2]
    plt.plot(data_far_1to10Hz['freq'][driven_freq],
             data_far_1to10Hz['FFT_flux_far_' + str(i + 1) + '_theo'][driven_freq],
             color='k', linestyle='--', linewidth=0.5)

driven_freq = np.where((data_far_1to10Hz['freq'] >= 1 - 0.5) &
                           (data_far_1to10Hz['freq'] < 10 + 0.5))
plt.plot(data_far_1to10Hz['freq'][driven_freq], data_close_1to10Hz['FFT_noise4_theo'][driven_freq])
plt.title('Flux close')
plt.xlabel('Frequency (Hz)')
plt.ylabel('$V^2$/Hz')

plt.figure(2)
for i in range(10):
    driven_freq = np.where((data_far_1to10Hz['freq'] >= (i + 1) * 1 - 0.5) &
                           (data_far_1to10Hz['freq'] < (i + 1) * 1 + 0.5))
    plt.plot(data_far_1to10Hz['freq'][driven_freq],
             data_close_1to10Hz['FFT_flux_close_' + str(i + 1) + '_theo'][driven_freq],
             color='k', linestyle='--', linewidth=0.5)

driven_freq = np.where((data_far_1to10Hz['freq'] >= 1 - 0.5) &
                           (data_far_1to10Hz['freq'] < 10 + 0.5))
plt.plot(data_far_1to10Hz['freq'][driven_freq], data_close_1to10Hz['FFT_noise4_theo'][driven_freq])
plt.title('Flux close')
plt.xlabel('Frequency (Hz)')
plt.ylabel('$V^2$/Hz')

plt.figure(3)
for i in range(10):
    driven_freq = np.where((data_far_10to100Hz['freq'] >= (i + 1) * 10 - 5) &
                           (data_far_10to100Hz['freq'] < (i + 1) * 10 + 5))
    plt.plot(data_far_10to100Hz['freq'][driven_freq],
             data_far_10to100Hz['FFT_flux_far_' + str(i + 1) + '_theo'][driven_freq],
             color='k', linestyle='--', linewidth=0.5)

driven_freq = np.where((data_far_10to100Hz['freq'] >= 10 - 5) & (data_far_10to100Hz['freq'] < 100 + 5))
plt.plot(data_far_10to100Hz['freq'][driven_freq], data_close_10to100Hz['FFT_noise4_theo'][driven_freq])
plt.title('Flux far')
plt.xlabel('Frequency (Hz)')
plt.ylabel('$V^2$/Hz')

plt.figure(4)
for i in range(10):
    driven_freq = np.where((data_far_10to100Hz['freq'] >= (i + 1) * 10 - 5) &
                           (data_far_10to100Hz['freq'] < (i + 1) * 10 + 5))
    plt.plot(data_far_10to100Hz['freq'][driven_freq],
             data_close_10to100Hz['FFT_flux_close_' + str(i + 1) + '_theo'][driven_freq],
             color='k', linestyle='--', linewidth=0.5)

driven_freq = np.where((data_far_10to100Hz['freq'] >= 10 - 5) & (data_far_10to100Hz['freq'] < 100 + 5))
plt.plot(data_far_10to100Hz['freq'][driven_freq], data_close_10to100Hz['FFT_noise4_theo'][driven_freq])
plt.title('Flux close')
plt.xlabel('Frequency (Hz)')
plt.ylabel('$V^2$/Hz')

plt.show()

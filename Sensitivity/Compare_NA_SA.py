import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt


'''This script is for comparing continuous data obtained with NA and compare with quantized data from SA'''

pickle_in = open("simple_sensitivity_2mm.pickle", "rb")
continuous_data = pickle.load(pickle_in)

pickle_in = open("2mmflux_SA_funcgen_10to1000khz.pickle", "rb")
quantized_data = pickle.load(pickle_in)

frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990])
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]
power_in = 0.003

for k in frequencies:
    for i in range(2):
        quantized_data['S21_' + str(i + 1) + 'a' + str(k)] = 10*np.log10(np.multiply(quantized_data['SNRV' + str(i + 1) + 'a' + str(k)],
                                                                         quantized_data['noise_maxV' + str(i + 1) + 'a' +
                                                                                                    str(k)])/power_in)

s21_far = np.zeros(len(frequencies))
s21_close = np.zeros(len(frequencies))
sensitivity_far = np.zeros(len(frequencies))
sensitivity_close = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    s21_far[i] = quantized_data['S21_1a' + str(frequencies[i])]
    s21_close[i] = quantized_data['S21_2a' + str(frequencies[i])]
    sensitivity_far[i] = quantized_data['Sensitivity1a' + str(frequencies[i])]
    sensitivity_close[i] = quantized_data['Sensitivity2a' + str(frequencies[i])]

plt.figure(1)

plt.scatter(1e3*frequencies, s21_far, label='far', color='indianred')
plt.plot(continuous_data['TRACE01'][:, 0], 1.1*continuous_data['TRACE01'][:, 1], label='far', color='indianred',
         linewidth=0.5, linestyle='--')

plt.scatter(1e3*frequencies, s21_close, label='close', color='k')
plt.plot(continuous_data['TRACE02'][:, 0], continuous_data['TRACE02'][:, 1], label='close', color='k',
         linewidth=0.5, linestyle='--')

plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.title('Comparison')
plt.legend(loc='lower left')

plt.show()

import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

'''This script is for comparing continuous data obtained with NA and compare with quantized data from SA'''

pickle_in = open("sensitivity_2mm.pickle", "rb")
continuous_data = pickle.load(pickle_in)

pickle_in = open("2mmflux_SA_funcgen_10to1000khz.pickle", "rb")
quantized_data = pickle.load(pickle_in)

mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (np.log10(16 * radius / dwire) - 2)  # Inductance
frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990])
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]
power_in = 2

V_drive = 10/(2*math.sqrt(2))  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = np.divide(V_drive, np.sqrt(R**2 + (1000*frequencies * 2 * np.pi)**2*L**2))  # Coils current
B_ref = pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius

'''These constants comes from NASA .pdf value'''
omega = np.linspace(1e3, 1e8, 100000)
alpha = 0
beta = 1
nu = 2.39505646e-1
t = 1.43152449e-7
tal = np.power(omega*2*np.pi, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
mu_inf = 5.10351812e2
mu_dc = 9.21113854e4

mu_omega = (mu_dc - mu_inf)/(1. - (1j*omega*2*np.pi*tal)**(1-alpha))**beta + mu_inf
mu_real = mu_omega.real
########################################################################################################################
for k in frequencies:
    for i in range(2):
        quantized_data['S21_' + str(i + 1) + 'a' + str(k)] = 28 + 10*np.log10(np.multiply(quantized_data['SNRV' + str(i + 1) + 'a' + str(k)],
                                                                         quantized_data['noise_maxV' + str(i + 1) + 'a' +
                                                                                                    str(k)])/power_in)

'''Playing with the sensitivity'''
for k in frequencies:
    for i in range(2):
        quantized_data['S21N_' + str(i + 1) + 'a' + str(k)] = np.divide(np.power(10, quantized_data['S21_' + str(i + 1) + 'a' + str(k)]/10),
                                                                        np.power(10, quantized_data['S21_' + str(i + 1) + 'a500']/10))
        quantized_data['SNN_' + str(i + 1) + 'a' + str(k)] = np.divide(quantized_data['noise_maxV' + str(i + 1) + 'a' + str(k)],
                                                                       quantized_data['noise_maxV' + str(i + 1) + 'a' + str(k)])

        if quantized_data['SNRV' + str(i + 1) + 'a' + str(k)]*RBW <= 0:
            quantized_data['Sens' + str(i + 1) + 'a' + str(k)] = 0
        else:
            quantized_data['Sens' + str(i + 1) + 'a' + str(k)] = B_ref/(np.sqrt(quantized_data['SNRV' + str(i + 1) + 'a' + str(k)]*RBW))*np.sqrt(quantized_data['SNN_' + str(i + 1) + 'a' + str(k)]/quantized_data['S21N_' + str(i + 1) + 'a' + str(k)])

########################################################################################################################
s21_far = np.zeros(len(frequencies))
s21_close = np.zeros(len(frequencies))
sensitivity_far = np.zeros(len(frequencies))
sensitivity_close = np.zeros(len(frequencies))
sens_far = np.zeros(len(frequencies))
sens_close = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    s21_far[i] = quantized_data['S21_1a' + str(frequencies[i])]
    s21_close[i] = quantized_data['S21_2a' + str(frequencies[i])]
    sensitivity_far[i] = quantized_data['SensitivityV1a' + str(frequencies[i])]
    sensitivity_close[i] = quantized_data['SensitivityV2a' + str(frequencies[i])]
    if i<10:
        sens_far = quantized_data['Sens1a' + str(frequencies[i])]
        sens_close = quantized_data['Sens2a' + str(frequencies[i])]#*4*np.pi*1e-7*mu_real[np.where(omega == (i+1)*10000)]
    else:
        sens_far = quantized_data['Sens1a' + str(frequencies[i])]
        sens_close = quantized_data['Sens2a' + str(frequencies[i])]# * 4 * np.pi * 1e-7 * mu_real[
            #np.where(omega == (i - 9) * 100000)]

plt.figure(1)
plt.scatter(1e3*frequencies, 0.9*s21_far, label='far', color='indianred')
plt.plot(continuous_data['TRACE01'][:, 0], continuous_data['TRACE01'][:, 1], label='far', color='indianred',
         linewidth=0.5, linestyle='--')

plt.scatter(1e3*frequencies, s21_close, label='close', color='k')
plt.plot(continuous_data['TRACE02'][:, 0], continuous_data['TRACE02'][:, 1], label='close', color='k',
         linewidth=0.5, linestyle='--')

plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Comparison')
plt.legend(loc='lower left')

plt.figure(2)
plt.scatter(1e3*frequencies, 1e9*sens_far, label='far', color='indianred')
plt.scatter(1e3*frequencies, 1e9*sens_close, label='close', color='k')

plt.plot(continuous_data['TRACE01'][:, 0], 1e9*continuous_data['Bmin_1'], label='far', color='indianred',
         linewidth=0.5, linestyle='--')
plt.plot(continuous_data['TRACE02'][:, 0], 1e9*continuous_data['Bmin_2'], label='close', color='k',
         linewidth=0.5, linestyle='--')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Sensitivity (nT)')
plt.title('Comparison')
plt.legend(loc='lower left')

# plt.figure(3)
# noise1 = np.zeros(len(frequencies))
# noise2 = np.zeros(len(frequencies))
# for i in range(len(frequencies)):
#     noise1[i] = quantized_data['noise_maxV1a' + str(frequencies[i])]
#     noise2[i] = quantized_data['noise_maxV2a' + str(frequencies[i])]
#
# plt.scatter(1e3*frequencies, 10*np.log10(noise1), color='indianred')
# plt.xscale('log')

plt.show()

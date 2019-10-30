import pickle
import numpy as np
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_2mm.pickle", "rb") #load dictionary that contains sensitivity measurements using NA (09-08-19)
continuous_data = pickle.load(pickle_in)

pickle_in = open("2mmflux_SA_funcgen_10to1000khz.pickle", "rb") #load dictionary that contains sensitivity measurements using SA (10-10-19)
quantized_data = pickle.load(pickle_in)

frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990]) #freq driving the coil
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800] #freq driving the coil for pick up testing
power_in = 0.003 #Power in the coil (the actual value is 0.13, but I use 0.003 to fit the conversion from SA to S21)

for k in frequencies:
    for i in range(2):
        quantized_data['S21_' + str(i + 1) + 'a' + str(k)] = 10*np.log10(np.multiply(quantized_data['SNRV' + str(i + 1) + 'a' + str(k)],
                                                                         quantized_data['noise_maxV' + str(i + 1) + 'a' +
                                                                                                    str(k)])/power_in)

signal_far = np.zeros(len(frequencies))
signal_close = np.zeros(len(frequencies))
s21_far = np.zeros(len(frequencies))
s21_close = np.zeros(len(frequencies))
sensitivity_far = np.zeros(len(frequencies))
sensitivity_close = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    signal_far[i] = quantized_data['signal1a' + str(frequencies[i])]
    signal_close[i] = quantized_data['signal2a' + str(frequencies[i])]
    s21_far[i] = quantized_data['S21_1a' + str(frequencies[i])]
    s21_close[i] = quantized_data['S21_2a' + str(frequencies[i])]
    sensitivity_far[i] = quantized_data['SensitivityV1a' + str(frequencies[i])]
    sensitivity_close[i] = quantized_data['SensitivityV2a' + str(frequencies[i])]

'''These constants comes from NASA .pdf value'''
omega = np.linspace(1e2, 1e8, 1000000)
alpha = 0
beta = 1
nu = 2.39505646e-1
t = 4.63152449e-6
tal = np.power(2*np.pi*omega, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
mu_inf = 5.10351812e2
mu_dc = 9.21113854e4

mu_omega = (mu_dc - mu_inf)/(1. - (1j*2*np.pi*omega*tal)**(1-alpha))**beta + mu_inf
mu_real = mu_omega.real
mu_imaginary = mu_omega.imag
mu_prime_imag = np.diff(mu_imaginary, 1)
mu_two_prime_imag = np.diff(mu_prime_imag, 1)

'''To compare sensitivity with and without flux conc., here, I am multiplying the sensitivity without flux by the real
part of the complex permeability to see if it fits the sensitivity with the flux concentrator'''
sensitivity_far_fit = np.zeros(len(frequencies))
for i in range(len(frequencies)):
    if i<10:
        sensitivity_far_fit[i] = sensitivity_far[i]*4*np.pi*1e-7*mu_real[np.where(omega == (i+1)*10000)]
    else:
        sensitivity_far_fit[i] = sensitivity_far[i] * 4 * np.pi * 1e-7 * mu_real[np.where(omega == (i - 9) * 100000)]
########################################################################################################################

# a = 0.2
# zero_imag = np.where((mu_prime_imag[:10000] >= -a) & (mu_prime_imag[:10000] <= a))
# print(zero_imag)
# print(omega[zero_imag])

# a = np.vstack((omega, mu_real))
# a = np.transpose(a)
#
# mu_prime_real = np.gradient(a)
# mu_two_prime_real = np.gradient(mu_prime_real)

# a=2.7e3
# b=92

fig, ax1 = plt.subplots()

ax1.plot(omega, mu_real, color='red', linestyle='--')
# ax1.plot(omega, 10*np.log10(omega**(-1.22)), color='red', linestyle='--')


ax2 = ax1.twinx()
# ax2.plot(continuous_data['TRACE02'][:, 0], continuous_data['TRACE02'][:, 1], label='close', color='k',
#          linewidth=0.5, linestyle='-')
ax2.scatter(1e3*frequencies, signal_close, label='close', color='k')

# plt.plot(omega, mu_imaginary, color='green', linestyle='--')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_ylim(0, 2e5)
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel(r'$\mu$')
ax2.set_ylim(-80, -55)
ax2.set_ylabel('PSD (dB)')

# fig.tight_layout()

# plt.figure(2)
# # plt.scatter(1e3*frequencies, 1e9*sensitivity_far, label='far', color='steelblue')
# plt.scatter(1e3*frequencies, 1e9*sensitivity_far_fit, label='far fit', color='k')
# plt.scatter(1e3*frequencies, 1e9*sensitivity_close, label='close', color='red')
# plt.xscale('log')
# plt.yscale('log')
# plt.ylim(100, 50000)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Sensitivity (nT)')
# plt.legend(loc='lower left')


# plt.figure(3)
# plt.plot(omega[1:-1], mu_two_prime, color='red', linestyle='--')
# plt.xscale('log')
#
plt.show()

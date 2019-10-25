import pickle
import numpy as np
import matplotlib.pyplot as plt

pickle_in = open("sensitivity_2mm.pickle", "rb")
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


omega = np.linspace(1e3, 1e8, 100000)
nu = 2.39505646e-1
t = 1.03152449e-6
tal = np.power(omega, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
mu_inf = 5.10351812e2
mu_dc = 9.21113854e4

mu_omega = (mu_dc - mu_inf)/(1. - 1j*omega*tal) + mu_inf
mu_real = mu_omega.real
mu_imaginary = mu_omega.imag
mu_prime_imag = np.diff(mu_imaginary, 1)
mu_two_prime_imag = np.diff(mu_prime_imag, 1)

# a = 0.2
# zero_imag = np.where((mu_prime_imag[:10000] >= -a) & (mu_prime_imag[:10000] <= a))
# print(zero_imag)
# print(omega[zero_imag])

# a = np.vstack((omega, mu_real))
# a = np.transpose(a)
#
# mu_prime_real = np.gradient(a)
# mu_two_prime_real = np.gradient(mu_prime_real)

a=2.7e3
b=92

fig, ax1 = plt.subplots()

ax1.plot(omega, mu_real/a-b, color='red', linestyle='--')


# ax2 = ax1.twinx()
# ax2.plot(continuous_data['TRACE02'][:, 0], continuous_data['TRACE02'][:, 1], label='close', color='k',
#          linewidth=0.5, linestyle='-')
ax1.scatter(1e3*frequencies, signal_close, label='close', color='k')

# plt.plot(omega, mu_imaginary, color='green', linestyle='--')
ax1.set_xscale('log')

# fig.tight_layout()
# plt.figure(2)
# plt.plot(a[:, 0], a[:, 1], color='red', linestyle='--')
# plt.xscale('log')

# plt.figure(3)
# plt.plot(omega[1:-1], mu_two_prime, color='red', linestyle='--')
# plt.xscale('log')
#
plt.show()

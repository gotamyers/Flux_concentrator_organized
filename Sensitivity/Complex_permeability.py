import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative

# (mu_dc - mu_inf)/(1. - 1j*omega*tal) + mu_inf
# tal = np.power(omega, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
# omega = np.linspace(1, 1e8, 1000000)
omega = np.linspace(1, 1e8, 100000)

nu = 2.39505646e-1
t = 4.63152449e-6
tal = np.power(omega, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
mu_inf = 5.10351812e2
mu_dc = 9.21113854e4

mu_omega = (mu_dc - mu_inf)/(1. - 1j*omega*tal) + mu_inf

mu_real = mu_omega.real
mu_imaginary = mu_omega.imag

mu_prime = np.diff(mu_real, 1)
mu_two_prime = np.diff(mu_prime, 1)


plt.figure(1)
plt.plot(omega, mu_real, color='red', linestyle='--')
plt.plot(omega, mu_imaginary, color='green', linestyle='--')
plt.xscale('log')
#
# plt.figure(2)
# plt.plot(omega[:-1], mu_prime, color='red', linestyle='--')
# plt.xscale('log')
#
# plt.figure(3)
# plt.scatter(omega, second, color='red')
# plt.xscale('log')
#
plt.show()

# import sympy as sp
# x = sp.Symbol('x')
# nu = 2.39505646e-1
# t = 4.63152449e-6
# mu_inf = 5.10351812e2
# mu_dc = 9.21113854e4
# tal_x = np.power(x, -nu)*pow(t, 1-nu)*np.exp(1j*nu*np.pi/2)
#
# mu_x = (mu_dc - mu_inf)/(1. - 1j*x*tal_x) + mu_inf
# mu_real = mu_x.real

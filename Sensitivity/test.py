from scipy.misc import derivative
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    o = (9.21113854e4 - 5.10351812e2)/(1. - 1j*x*2*np.pi*np.power(x*2*np.pi, -2.39505646e-1)*pow(4.63152449e-6, 1-2.39505646e-1)*np.exp(1j*2.39505646e-1*np.pi/2)) + 5.10351812e2
    return np.real(o)


def d(x):
    return x*2.303*derivative(f, x)


def d2(x):
    return derivative(d, x)


def d_f(x):
    p = np.real((9.21113854e4 - 5.10351812e2) / (
                1. - 1j * x * 2 * np.pi * np.power(x * 2 * np.pi, -2.39505646e-1) * pow(4.63152449e-6,
                                                                                        1 - 2.39505646e-1) * np.exp(
            1j * 2.39505646e-1 * np.pi / 2)) + 5.10351812e2)
    g = np.log10(p)
    return np.gradient(g, np.log10(x))


y = np.linspace(1e2, 1e9, 1000000)
print(derivative(f, 206000))

plt.figure(1)
plt.plot(2*np.pi*y, f(y))
plt.plot(2*np.pi*y, 12212.4*(2*np.pi*y/1.3e6)**(-0.84))
plt.ylim(5e2, 2e5)
plt.xscale('log')
plt.yscale('log')
plt.ylabel(r'$\mu$')
plt.xlabel('Frequency (Hz)')

plt.figure(2)
plt.plot(y,d(y))
#
plt.figure(3)
plt.plot(y,d2(y))

# plt.figure(4)
# plt.plot(y,d_f(y))
# plt.xscale('log')

plt.show()

from scipy.misc import derivative

def f(x):
    # o = (9.21113854e4 - 5.10351812e2)/(1. - 1j*x*np.power(x, -2.39505646e-1)*pow(4.63152449e-6, 1-2.39505646e-1)*np.exp(1j*2.39505646e-1*np.pi/2)) + 5.10351812e2
    o = np.cos(x)
    return np.real(o)

def d(x):
    return derivative(f,x)

def d2(x):
    return derivative(d,x)

import matplotlib.pyplot as plt
import numpy as np

y = np.linspace(0, 10, 10000)
plt.figure(1)
plt.plot(y, f(y))
# plt.xscale('log')

plt.figure(2)
plt.plot(y,d(y))

plt.figure(3)
plt.plot(y,d2(y))

plt.show()

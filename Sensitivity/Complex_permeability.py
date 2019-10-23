import pickle
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1e4, 1e6, 100)
omega = x
tal = 1e-7
mu_inf = 5.1e2
mu_dc = 9.2e4

mu_line = (mu_dc - mu_inf) / (1 + omega**2*pow(tal,2)) + mu_inf
mu_twolines = omega*tal*(mu_dc - 1) / (1 + omega**2*pow(tal,2))

mu_omega = mu_line + 1j * mu_twolines

plt.figure(1)
plt.plot(x, mu_line)
# plt.plot(x, mu_twolines, color='k')

plt.show()

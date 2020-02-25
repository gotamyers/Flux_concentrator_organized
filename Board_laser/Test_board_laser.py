import pickle
import numpy as np
import matplotlib.pyplot as plt

pickle_in = open("avg_dB_FFT_noise.pickle", "rb")
data_noise = pickle.load(pickle_in)

pickle_in = open("avg_dB_FFT0_plot.pickle", "rb")
data = pickle.load(pickle_in)

mask = data_noise['freq'] > 0


plt.figure(1)
plt.plot(data_noise['freq'][mask], data['avg_dB_FFT_scope_noise_theo'][mask])
plt.plot(data_noise['freq'][mask], data_noise['avg_dB_FFT_scope_theo'][mask])

plt.xlim(9e3, 0.1e6)
plt.ylim(-80, -50)

plt.show()


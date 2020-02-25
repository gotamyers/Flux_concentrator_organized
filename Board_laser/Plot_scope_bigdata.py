import pickle
import numpy as np
import matplotlib.pyplot as plt


for i in range(8):
    pickle_in = open("dB_avg_FFT_scope_theo_" + str(i) + ".pickle", "rb")
    data_plot = pickle.load(pickle_in)
    mask = data_plot['freq'] > 0
    # a1 = data_plot['freq'][mask]
    # print(a1[3] - a1[2])

    '''Plot test'''
    plt.figure(1)
    plt.plot(data_plot['freq'][mask], data_plot['dB_avg_FFT_scope_theo'][mask])

plt.xlim(100e3, 0.2e6)
plt.ylim(-150, -90)


pickle_in = open("dB_avg_FFT_noise.pickle", "rb")
data_plot = pickle.load(pickle_in)

mask = data_plot['freq'] > 0

pickle_in = open("dB_avg_FFT_scope_theo_0.pickle", "rb")
data1 = pickle.load(pickle_in)


plt.figure(2)
plt.plot(data_plot['freq'][mask], data_plot['dB_avg_FFT_scope_noise_theo'][mask], color='k')
plt.plot(data_plot['freq'][mask], data1['dB_avg_FFT_scope_theo'][mask])

plt.xlim(100e3, 0.2e6)
plt.ylim(-150, -90)


plt.show()

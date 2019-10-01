import numpy as np
import pickle
import matplotlib.pyplot as plt


pickle_in = open("2mmflux_close_1to10Hz.pickle", "rb")
data_close_1to10Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_1to10Hz.pickle", "rb")
data_far_1to10Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_close_10to100Hz.pickle", "rb")
data_close_10to100Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_10to100Hz.pickle", "rb")
data_far_10to100Hz = pickle.load(pickle_in)

freq1 = np.arange(10)+1
freq2 = (np.arange(10) + 1)*10


'''Plot sensitivity'''
plt.figure(1)
for i in range(10):
    plt.plot(freq1[i], data_close_1to10Hz['Bmin' + str(i)], marker='o', color='b', label='close')
    plt.plot(freq1[i], data_far_1to10Hz['Bmin' + str(i)], marker='o', color='r', label='far')
    plt.plot(freq2[i], data_close_10to100Hz['Bmin' + str(i)], color='b', marker='o')
    plt.plot(freq2[i], data_far_10to100Hz['Bmin' + str(i)], marker='o', color='r')
    plt.xlim(0.6, 200)
    plt.ylim(1e-6, 0.01)

plt.xscale('log')
plt.yscale('log')


plt.show()

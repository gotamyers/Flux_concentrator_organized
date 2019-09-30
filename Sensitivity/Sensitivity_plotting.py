import math
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

pickle_in = open("2mmflux_close_100to1000Hz.pickle", "rb")
data_close_100to1000Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_100to1000Hz.pickle", "rb")
data_far_100to1000Hz = pickle.load(pickle_in)

pickle_in = open("sensitivity_1000to10000Hz.pickle", "rb")
sensitivity_1000to10000Hz = pickle.load(pickle_in)


# mask = data_close_1to10Hz['freq'] > 0

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 200, 300, 400, 500, 600, 700, 800,
     900, 1000, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
sensitivity_close_1to10Hz = []
sensitivity_close_10to100Hz = []
sensitivity_close_100to1000Hz = []
sensitivity_far_1to10Hz = []
sensitivity_far_10to100Hz = []
sensitivity_far_100to1000Hz = []


for i in range(10):
    sensitivity_close_1to10Hz = np.append(sensitivity_close_1to10Hz, data_close_1to10Hz['Bmin' + str(i + 1)])
    sensitivity_close_10to100Hz = np.append(sensitivity_close_10to100Hz, data_close_10to100Hz['Bmin' + str(i + 1)])
    sensitivity_close_100to1000Hz = np.append(sensitivity_close_100to1000Hz,
                                              data_close_100to1000Hz['Bmin' + str(i + 1)])
    sensitivity_far_1to10Hz = np.append(sensitivity_far_1to10Hz, data_far_1to10Hz['Bmin' + str(i + 1)])
    sensitivity_far_10to100Hz = np.append(sensitivity_far_10to100Hz, data_far_10to100Hz['Bmin' + str(i + 1)])
    sensitivity_far_100to1000Hz = np.append(sensitivity_far_100to1000Hz, data_far_100to1000Hz['Bmin' + str(i + 1)])

sensitivity_close = np.append(sensitivity_close_1to10Hz, [sensitivity_close_10to100Hz, sensitivity_close_100to1000Hz,
                                                          sensitivity_1000to10000Hz['sensitivity_close_1000to10000Hz']])
sensitivity_far = np.append(sensitivity_far_1to10Hz, [sensitivity_far_10to100Hz, sensitivity_far_100to1000Hz,
                                                      sensitivity_1000to10000Hz['sensitivity_far_1000to10000Hz']])

'''Plot sensitivity'''
plt.figure(1)
plt.scatter(x, sensitivity_close, label='close')
plt.scatter(x, sensitivity_far, label='far')
# plt.xlim(0.5, 10.5)
plt.ylim(0.00001, 0.002)
plt.xscale('log')
plt.yscale('log')
plt.legend(loc='upper right')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Sensitivity T/Hz')
# plt.title('20 khz - far')
#
# plt.figure(12)
# plt.plot(data['freq'][mask], 1e3*data['FFT_noise4_theoretical'][mask])
# plt.xlim(0.5, 10.5)
# plt.ylim(0, 0.70)
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('mV')
# plt.title('Noise')
#
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import pickle
import numpy.polynomial.polynomial as poly
import scipy.optimize

# def smooth(y, box_pts):
#     box = np.ones(box_pts)/box_pts
#     y_smooth = np.convolve(y, box, mode='same')
#     return y_smooth

data = {}
# n_smooth = 70
tags = ['1-elec noise', '2-shot noise', '3-(a) stretcher plugged in / (b) 0m', '4-(a) stretcher / (b) 0m', '5-balanced long (a) stretcher / (b) 17m fibre',
        '6-(a) 0m / (b) 17m fibre', '7-balanced short (a) 0m / (b) 0m', '8-balanced long (a) stretcher / (b) 16m fibre', '9-balanced long (a) 16m / (b) 16m', '10-balanced long (a) 16m / (b) 16m']



for a in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    k = a+1
    ref_data = np.fromfile("C:/Users/uqfgotar/Documents/Magnetometry/Board_laser/20200820/testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)
    data["freq" + str(k)] = ref_data[0] + ref_data[1] * np.array(range(len(ref_data[2:])))
    data["PSD" + str(k)] = np.fromfile(
        "C:/Users/uqfgotar/Documents/Magnetometry/Board_laser/20200820/testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

plt.figure(1)
for a in [1, 4, 6, 7, 9]:
    k = a+1
    plt.plot(data["freq" + str(k)], data["PSD" + str(k)], label=str(tags[k-1]))

plt.xlim(1, 4e4)
plt.ylim(-120, -10)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
# plt.title("Phase noise coefficients")
plt.legend(loc='upper right')

plt.figure(2)
for a in [1, 3, 5]:
    k = a+1
    plt.plot(data["freq" + str(k)], data["PSD" + str(k)], label=str(tags[k-1]))

plt.xlim(1, 4e4)
plt.ylim(-120, -10)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
# plt.title("Phase noise coefficients")
plt.legend(loc='upper right')
#

plt.figure(3)
for a in [1, 6, 9]:
    k = a+1
    plt.plot(data["freq" + str(k)], data["PSD" + str(k)], label=str(tags[k-1]))

plt.xlim(1, 4e4)
plt.ylim(-120, -10)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
# plt.title("Phase noise coefficients")
plt.legend(loc='upper right')

# plt.figure(4)
# for k in range(3):
#     plt.plot(data["freq"], data["PSD" + str(k + 6)], label=str(tags[k+5]))
#
# plt.xlim(1, 1e5)
# plt.ylim(-160, -60)
# plt.xscale('log')
#
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD')
# # plt.title("Phase noise coefficients")
# plt.legend(loc='upper right')
#
# plt.figure(5)
# for k in [6, 10]:
#     plt.plot(data["freq"], data["PSD" + str(k)], label=str(tags[k-1]))
#
# plt.xlim(1, 1e5)
# plt.ylim(-160, -60)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD')
# # plt.title("Phase noise coefficients")
# plt.legend(loc='upper right')


plt.show()

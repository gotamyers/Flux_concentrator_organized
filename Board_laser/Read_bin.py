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
tags = ['9 Vpp @ 1kHz', '5 Vpp @ 1kHz', '1 Vpp @ 1kHz', 'modulation off', 'laser off', 'balanced with 9Vpp @ 1kHz']



for k in [2, 7]:
    ref_data = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\20200819\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)
    data["freq" + str(k)] = ref_data[0] + ref_data[1] * np.array(range(len(ref_data[2:])))

    data["PSD" + str(k)] = np.fromfile(
        "C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\20200819\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

plt.figure(1)
for k in [2, 7]:
    plt.plot(data["freq" + str(k)], data["PSD" + str(k)], label=str(tags[k-2]))

plt.xlim(1, 3e4)
plt.ylim(-130, -30)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD')
# plt.title("Phase noise coefficients")
plt.legend(loc='upper right')

# plt.figure(2)
#
# plt.plot(data["freq"], data["PSD10"], label='high power')
# plt.plot(data["freq"], data["PSD8"], label='electronics')
#
# plt.xlim(1, 1.2e6)
# plt.ylim(-160, -60)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD')
# plt.title("Phase noise coefficients")
# plt.legend(loc='upper right')
#
#
#
#
# plt.figure(3)
# for k in range(5):
#     plt.plot(data["freq"], data["PSD" + str(k + 6)], label=str(tags[k+5]))
#
# plt.xlim(1, 1.2e6)
# plt.ylim(-160, -60)
# plt.xscale('log')
#
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD')
# # plt.title("Phase noise coefficients")
# plt.legend(loc='upper right')
#
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

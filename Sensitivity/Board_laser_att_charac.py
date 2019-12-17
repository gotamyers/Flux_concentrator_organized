import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import simps

pickle_in = open("board_laser_attenuator_charact.pickle", "rb")
data_attenuator = pickle.load(pickle_in)

power = np.asarray([2.1, 1.6, 1.1, 0.6, 0.1, 0.05, 0.0])
points = np.linspace(119, 701, 15, dtype=int)
freq = np.zeros(len(points))
for k in range(len(points)):
    freq[k] = data_attenuator['LPD1'][points[k], 0]

selec_power = np.zeros([7, len(points)])
selec_powerV = np.zeros([7, len(points)])
for k in range(len(points)):
    for i in range(7):
        selec_power[i, k] = data_attenuator['LPD' + str(i + 1)][points[k], 1]
        selec_powerV[i, k] = np.power(10, data_attenuator['LPD' + str(i + 1)][points[k], 1] / 10)

what = selec_powerV[:, 13]

# This is the function we are trying to fit to the data.
def fitting(x, b, c):
    return b*x + c


'''Integrating 2D array for a certain delta_omega'''
N = 75
integral_points = int(len(data_attenuator['LPD1'][:, 0])/N)
print(integral_points)
delta_omega = np.zeros(integral_points)
integral = np.zeros([len(power), integral_points])
for l in range(len(power)):
    for i in range(integral_points-1):
        f_k = 0.
        delta_omega[i] = data_attenuator['LPD1'][(i + 1)*N, 0] - data_attenuator['LPD1'][i*N, 0]
        for k in range(N):
            f_k = f_k + data_attenuator['LPD_V' + str(l + 1)][k + i*N]
        integral[l, i] = delta_omega[i]*f_k/N

print(integral.shape)


m = 7
'''Plot signal'''
colors = ['black', 'firebrick', 'sandybrown', 'olivedrab', 'lightblue', 'blue', 'darkviolet', 'pink']
plt.figure(1)
# for k in range(len(points)):
#     plt.scatter(power, selec_powerV[:, k], label=str(points[k]))
plt.scatter(power, integral[:, m], label='86.7 MHz')
# plt.xlim(9000, 100e6)
plt.ylim(0, 4e-3)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper left')
plt.xlabel('Power (mW)')
plt.ylabel('PSD (not dB)')
# plt.title('Spectrum analyser signal')

# The actual curve fitting happens here
param, param_cov = curve_fit(fitting, power, integral[:, m])
print(param)
# print(param_cov)
ans = (param[0]*power + param[1])
# Use the optimized parameters to plot the best fit
plt.plot(power, ans, label="fit")

plt.show()

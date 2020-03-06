import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


data = {}

power = [0.0, 20, 40, 60, 80, 100, 120]
n_smooth = 100

########################################################################################################################
'''Read data'''
for k in range(8):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
              + '\\SSA_' + str(k) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['LPD' + str(k)] = np.array(df)
    data['LPD_V' + str(k)] = np.power(10, data['LPD' + str(k)][:, 1])

# for k in range(6):
#     data['LPD_V' + str(k+2)] = data['LPD_V' + str(k+2)]*power[k + 1]

# print(data['LPD' + str(k)][point, 0], data['LPD' + str(k + 1)][point + delta_freq, 0])
# with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\24thFeb2020'
#           + '\\SSA_noise.csv') as a:
#     df = csv.reader(a, delimiter=',')
#     df_temp = []
#     for row in df:
#         df_temp.append(row)
#     df = df_temp[31:]
#     for j in range(len(df)):
#         df[j] = [np.float(df[j][0]), np.float(df[j][1])]
#
# data['SA_noise'] = np.array(df)
# data['SA_noise_V'] = np.power(10, data['SA_noise'][:, 1] / 10)

data['smooth_LPD_V0'] = smooth(data['LPD_V0'], n_smooth)
data['smooth_LPD0'] = 10*np.log10(data['smooth_LPD_V0'])
for k in range(7):
    data['smooth_LPD_V' + str(k + 1)] = smooth(data['LPD_V' + str(k + 1)], n_smooth)
    data['smooth_LPD_V' + str(k + 1)] = np.abs(data['smooth_LPD_V' + str(k + 1)] - data['smooth_LPD_V0'])
    data['smooth_LPD' + str(k + 1)] = 10*np.log10(data['smooth_LPD_V' + str(k + 1)])


coef_x_square = np.zeros(len(data['smooth_LPD0']))
coef_x_lin = np.zeros(len(data['smooth_LPD0']))

for k in range(len(data['smooth_LPD0'])):
    LPD_V_notdB = np.zeros(len(power))

    for i in range(len(power)):
        LPD_V_notdB[i] = data['smooth_LPD_V' + str(i + 1)][k]

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
    coefs = poly.polyfit(power, LPD_V_notdB, 2)
    ffit = poly.Polynomial(coefs)
    # plt.plot(x_new, ffit(x_new))
    coef_x_square[k] = coefs[2]
    coef_x_lin[k] = coefs[1]

ratio = coef_x_square/coef_x_lin

plt.figure(2)
plt.plot(data['LPD0'][:, 0], ratio)
# plt.ylim(0, 1)

plt.figure(3)
plt.plot(data['LPD0'][:, 0], coef_x_square)
plt.plot(data['LPD0'][:, 0], coef_x_lin, color='k')


plt.figure(1)
for k in range(7):
    plt.plot(data['LPD0'][:, 0], data['smooth_LPD' + str(k + 1)])

plt.show()

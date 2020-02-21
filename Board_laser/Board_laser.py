import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

data = {}

power = [0., 20.4, 40.4, 60.4, 79.7, 99.8, 114.3]
point = 200
delta_freq = 30
########################################################################################################################
'''Read data'''
for k in range(8):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thFeb2020'
              + '\\SSA_1)0' + str(k) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['LPD' + str(k)] = np.array(df)
    data['LPD_V' + str(k)] = np.power(10, data['LPD' + str(k)][:, 1]/10)

# print(data['LPD' + str(k + 1)][point, 0])
with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thFeb2020'
          + '\\SSA_1)noise.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

data['SA_noise'] = np.array(df)
data['SA_noise_V'] = np.power(10, data['SA_noise'][:, 1] / 10)

'''Subtracting electronical noise and averaging on a range of frequencies'''
for k in range(7):
    data['LPD_V' + str(k + 1)] = data['LPD_V' + str(k + 1)] - data['SA_noise_V']
    data['LPD_V_avg' + str(k + 1)] = data['LPD_V' + str(k + 1)][point:point + delta_freq]
    data['LPD_V_avg' + str(k + 1)] = np.average(data['LPD_V_avg' + str(k + 1)])
########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("board_laser_attenuator_charact.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Plot signal'''
colors = ['black', 'firebrick', 'sandybrown', 'olivedrab', 'lightblue', 'blue', 'darkviolet', 'pink']
plt.figure(1)
# plt.plot(data['SA_noise'][:, 0], data['SA_noise'][:, 1], label='SA noise')
for k in range(5):
    plt.plot(data['LPD' + str(k + 1)][:, 0], data['LPD' + str(k + 1)][:, 1], label=str(power[k]) + ' uW')

plt.xlim(9000, 1e6)
plt.ylim(-105, -90)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Spectrum analyser signal')

plt.figure(2)
LPD_V_notdB = np.zeros(5)
for k in range(5):
    plt.scatter(power[k], data['LPD_V_avg' + str(k + 1)], color='k')
    LPD_V_notdB[k] = data['LPD_V_avg' + str(k + 1)]
# plt.xlim(9000, 100e6)
plt.ylim(0, 5e-10)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Power (mW)')
plt.ylabel('PSD (not dB)')
plt.title('Spectrum analyser signal')

'''Fitting polynomial to figure (2)'''
x_new = np.linspace(power[0], power[-1], num=len(power)*10)
coefs = poly.polyfit(power[:-2], LPD_V_notdB, 2)
ffit = poly.Polynomial(coefs)
plt.plot(x_new, ffit(x_new))
print(coefs)



plt.show()

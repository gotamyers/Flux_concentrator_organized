import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

data = {}

power = [0.0, 0.25, 0.50, 0.75, 1.25, 1.50, 1.75]
########################################################################################################################
'''Read data'''
for k in range(7):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\4thFeb2020'
              + '\\SSA_1' + str(k + 1) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['LPD' + str(k + 1)] = np.array(df)
    data['LPD_V' + str(k + 1)] = np.power(10, data['LPD' + str(k + 1)][:, 1]/10)


with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\4thFeb2020'
          + '\\SSA_10.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

data['SA_noise'] = np.array(df)
data['SA_noise_V'] = np.power(10, data['SA_noise'][:, 1] / 10)

with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\4thFeb2020'
          + '\\SSA_noise1.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

data['just_SA'] = np.array(df)
data['just_SA_V'] = np.power(10, data['just_SA'][:, 1] / 10)
########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("board_laser_attenuator_charact.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''Plot signal'''
colors = ['black', 'firebrick', 'sandybrown', 'olivedrab', 'lightblue', 'blue', 'darkviolet', 'pink']
plt.figure(1)
for k in range(7):
    plt.plot(data['LPD' + str(k + 1)][:, 0], data['LPD' + str(k + 1)][:, 1], label=str(power[k]))
plt.plot(data['SA_noise'][:, 0], data['SA_noise'][:, 1], label='Elec. noise')
plt.xlim(9000, 1e6)
plt.ylim(-130, -80)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Spectrum analyser signal')

plt.figure(2)
LPD_V_notdB = np.zeros(7)
for k in range(7):
    plt.scatter(power[k], data['LPD_V' + str(k + 1)][720], color='k')
    LPD_V_notdB[k] = data['LPD_V' + str(k + 1)][720]
# plt.xlim(9000, 100e6)
plt.ylim(0, 1e-10)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Power (mW)')
plt.ylabel('PSD (not dB)')
plt.title('Spectrum analyser signal')

'''Fitting polynomial to figure (2)'''
x_new = np.linspace(power[0], power[-1], num=len(power)*10)
coefs = poly.polyfit(power, LPD_V_notdB, 1)
ffit = poly.Polynomial(coefs)
plt.plot(x_new, ffit(x_new))
print(coefs)


plt.figure(3)
plt.plot(data['just_SA'][:, 0], data['just_SA'][:, 1], label='SA noise')
plt.plot(data['SA_noise'][:, 0], data['SA_noise'][:, 1], label='Elec. noise')
plt.xlim(9000, 1e6)
plt.ylim(-130, -80)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Spectrum analyser signal')

plt.show()

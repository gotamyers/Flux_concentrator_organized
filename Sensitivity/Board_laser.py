import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

data = {}

power = [2.1, 1.6, 1.1, 0.6, 0.1, 0.05, 0.0]
########################################################################################################################
'''Read data'''
for k in [1, 2, 3]:
# with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\29thNov'
              + '\\SSA_2' + str(k) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]
        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['retakenLPD' + str(k)] = np.reshape(np.array(df), (-1, 2))
    data['retakenLPD' + str(k)] = np.array(df)
    data['retakenLPD_V' + str(k)] = np.power(10, data['retakenLPD' + str(k)][:, 1]/10)

for k in range(7):
# with open('C:\\Users\\Fernando\\Documents\\Phd\\10thOct'
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\29thNov'
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
data['LPD1'] = data['retakenLPD1']
data['LPD2'] = data['retakenLPD2']
data['LPD_V1'] = np.power(10, data['retakenLPD1'][:, 1]/10)
data['LPD_V2'] = np.power(10, data['retakenLPD2'][:, 1]/10)

with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\29thNov'
          + '\\SSA_00.csv') as a:
    df = csv.reader(a, delimiter=',')
    df_temp = []
    for row in df:
        df_temp.append(row)
    df = df_temp[31:]
    for j in range(len(df)):
        df[j] = [np.float(df[j][0]), np.float(df[j][1])]

data['SA_noise'] = np.array(df)
data['SA_noise_V'] = np.power(10, data['SA_noise'][:, 1] / 10)
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
plt.xlim(9000, 100e6)
plt.ylim(-115, -65)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Spectrum analyser signal')

plt.figure(2)

plt.plot(data['LPD7'][:, 0], data['LPD7'][:, 1], label='0.0 mW')
plt.plot(data['SA_noise'][:, 0], data['SA_noise'][:, 1], label='SA noise')
plt.xlim(9000, 100e6)
plt.ylim(-125, -65)
# plt.xscale('log')
# plt.yscale('log')
plt.legend(loc='upper right')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dB)')
plt.title('Spectrum analyser signal')

plt.show()


import csv
import pickle
import numpy as np
import matplotlib.pyplot as plt


B = 5e-4
RBW = 30

data2 = {}
'''READ SPECTRUM ANALYZER .CSV FILES'''
for k in range(29):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\19thJul\\2dScan_190719_FG_JB'
              + '\\TRACE' + str("{:02d}".format(k+1)) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df[:][1])):
            df[j] = [np.float(df[j][0]), np.float(df[j][1]), np.float(df[j][2])]

    data2['TRACE' + str("{:02d}".format(k+1))] = np.array(df)
    data2['TRACE' + str("{:02d}".format(k + 1))] = data2['TRACE' + str("{:02d}".format(k+1))][:, :2]
    data2['TRACE' + str("{:02d}".format(k + 1))] = np.array(data2['TRACE' + str("{:02d}".format(k + 1))]).astype(np.float)

###########################################################################################################################################

'''SAVE DICTIONARY'''
# pickle_out = open("2d_scan_2mm.pickle", "wb")
# pickle.dump(data2, pickle_out)
# pickle_out.close()
###########################################################################################################################################
# x = np.around(np.linspace(-0.7, 0.7, 28), decimals=2)
# S21_y = np.zeros(29)
# for k in range(29):
#     S21_y[k] = data2['TRACE' + str("{:02d}".format(k + 1))][12, 1]
#
# plt.figure(1)
# plt.plot(x, S21_y[1:])
# plt.xlabel('y-position (mm)')
# plt.ylabel(r'S$_{21}$ (dB)')
#
# plt.show()

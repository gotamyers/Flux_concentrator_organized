import csv
import pickle
import numpy as np

'''This script is used for reading files saved as TRACE(number).csv and store it in a dictionary. In this case, it is
going to read data acquired using a 2 mm long flux concentrator as a function of height and frequency'''

data2 = {}
'''READ SPECTRUM ANALYZER .CSV FILES'''
for k in range(27):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\19thJul\\1dScan_190719_FG_JB'
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
pickle_out = open("1d_scan_2mm.pickle", "wb")
pickle.dump(data2, pickle_out)
pickle_out.close()
###########################################################################################################################################

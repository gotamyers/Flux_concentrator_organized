import csv
import pickle
import numpy as np

'''This script is used for reading files saved as TRACE(number).csv and store it in a dictionary. In this case, it is
going to read data acquired using a 5 mm long flux concentrator as a function of height and frequency'''

data5 = {}
'''READ SPECTRUM ANALYZER .CSV FILES'''
for k in range(28):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\6thAug\\1dScan_060819_FG_JB'
              + '\\TRACE' + str("{:02d}".format(k+1)) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df[:][1])):
            df[j] = [np.float(df[j][0]), np.float(df[j][1]), np.float(df[j][2])]

    data5['TRACE' + str("{:02d}".format(k+1))] = np.array(df)
    data5['TRACE' + str("{:02d}".format(k + 1))] = data5['TRACE' + str("{:02d}".format(k+1))][:, :2]
    data5['TRACE' + str("{:02d}".format(k + 1))] = np.array(data5['TRACE' + str("{:02d}".format(k + 1))]).astype(np.float)

###########################################################################################################################################

'''SAVE DICTIONARY'''
pickle_out = open("1d_scan_5mm.pickle", "wb")
pickle.dump(data5, pickle_out)
pickle_out.close()
###########################################################################################################################################
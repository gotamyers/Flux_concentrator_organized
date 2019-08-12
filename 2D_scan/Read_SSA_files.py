import csv
import pickle
import numpy as np

'''Can be used for reading files from the Spectrum analyzer, but we changed our system and started using the Network
Analyzer as a external trigger'''

B = 5e-4
RBW = 30

data = {}
'''READ SPECTRUM ANALYZER .CSV FILES and store in a dictionary named data'''
for k in range(22):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
              + '\\SSA_' + str("{:02d}".format(k+2)) + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

    data['SSA_' + str("{:02d}".format(k+2))] = np.array(df)
    data['SSA_' + str("{:02d}".format(k+2))] = data['SSA_' + str("{:02d}".format(k+2))][:, 1]

for k in range(2): #this part is separated from the one above just because the name of the .csv files was different
                    #it corresponds to the noise
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
              + '\\SSA_' + str("{:02d}".format(k)) + '_noise' + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['SSA_' + str("{:02d}".format(k)) + '_noise'] = np.reshape(np.array(df), (-1, 2))

    data['SSA_' + str("{:02d}".format(k)) + '_noise'] = np.array(df)
    data['SSA_' + str("{:02d}".format(k)) + '_noise'] = data['SSA_' + str("{:02d}".format(k)) + '_noise'][:, 1]

for k in range(2):#this part is separated from the one above just because the name of the .csv files was different
                    #it corresponds to the noise
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
              + '\\SSA_' + str("{:02d}".format(k)) + '_noise_ref' + '.csv') as a:
        df = csv.reader(a, delimiter=',')
        df_temp = []
        for row in df:
            df_temp.append(row)
        df = df_temp[31:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['SSA_' + str("{:02d}".format(k)) + '_noise_ref'] = np.reshape(np.array(df), (-1, 2))

    data['SSA_' + str("{:02d}".format(k)) + '_noise_ref'] = np.array(df)
    data['SSA_' + str("{:02d}".format(k)) + '_noise_ref'] = data['SSA_' + str("{:02d}".format(k)) + '_noise_ref'][:, 1]
###########################################################################################################################################

'''READ OSCILLOSCOPE .CSV FILES store in the same dictionary named data'''
for k in range(22):
    for i in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
                  + '\\Scope_' + str("{:02d}".format(k+2)) + '_Ch' + str(i+3) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row[:][3:])
            df = df_temp

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['Scope_' + str("{:02d}".format(k+2)) + '_Ch' + str(i+3)] = np.reshape(np.array(df), (-1, 2))

        data['Scope_' + str("{:02d}".format(k+2)) + '_Ch' + str(i+3)] = np.array(df)

for k in range(1): #this part is separeted from the one above just because the name of the .csv files was different
                    #it corresponds to the noise
    for i in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
                  + '\\Scope_' + str("{:02d}".format(k)) + '_noise' + '_Ch' + str(i+3) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row[:][3:])
            df = df_temp

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['Scope_' + str("{:02d}".format(k+2)) + '_noise' + '_Ch' + str(i+3)] = np.reshape(np.array(df), (-1, 2))

        data['Scope_' + str("{:02d}".format(k+2)) + '_noise' + '_Ch' + str(i+3)] = np.array(df)

for k in range(1): #this part is separeted from the one above just because the name of the .csv files was different
                    #it corresponds to the noise
    for i in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\254_4\\12thJuly'
                  + '\\Scope_' + str("{:02d}".format(k)) + '_noise_ref' + '_Ch' + str(i+3) + '.csv') as a:
            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row[:][3:])
            df = df_temp

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['Scope_' + str("{:02d}".format(k+2)) + '_noise_ref' + '_Ch' + str(i+3)] = np.reshape(np.array(df), (-1, 2))

        data['Scope_' + str("{:02d}".format(k+2)) + '_noise_ref' + '_Ch' + str(i+3)] = np.array(df)
###########################################################################################################################################

'''SAVE DICTIONARY'''
pickle_out = open("dict.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
###########################################################################################################################################

'''After running this script, go to script 'Exclude_SA_stopped_points.py' because it exclude the data acquired while
the stage was wait to start moving. This points only exists because this measurements were made while I was alone
at the lab, so I had to clock the difference in time between hitting the Single button at SA and then at the Scope and
finally at the Labview program'''
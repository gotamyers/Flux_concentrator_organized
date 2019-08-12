import pickle
import numpy as np
'''This script focuses in doing the math for plotting the data we saved. It also can ignores TRACE27 because it is just
electronical noise, i.e., no light was applied for saving this particular data.'''

'''Read dictionary'''
pickle_in = open("2d_scan_2mm.pickle", "rb")
data2 = pickle.load(pickle_in)

for k in range(28): #indenting this results in a 2D plot of the signal
    data2['TRACE' + str("{:02d}".format(k+1)) + '_gain'] = np.subtract(data2['TRACE' + str("{:02d}".format(k+1))][:, 1],
                                                                       data2['TRACE29'][:, 1])
# for k in range(27):
#     data2['TRACE' + str("{:02d}".format(k+1)) + '_gain'] = data2['TRACE' + str("{:02d}".format(k+1))][:, 1]

df_temp = np.zeros(shape=(28, 28))
for k in range(28):
    df_temp[:, k] = data2['TRACE' + str("{:02d}".format(k + 1)) + '_gain']
data2['TRACE_signal'] = df_temp

# '''takes the gain at frequency 550 kHz for each height for plotting it later'''
# df_temp = np.zeros(27)
# for k in range(27):
#     df_temp[k] = data2['TRACE' + str("{:02d}".format(k + 1)) + '_gain'][375]
# data2['decay_2mm'] = np.array(df_temp).astype(np.float)

###########################################################################################################################################

'''SAVE DICTIONARY'''
pickle_out = open("2d_scan_2mm.pickle2", "wb")
pickle.dump(data2, pickle_out)
pickle_out.close()
###########################################################################################################################################

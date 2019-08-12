import pickle
import numpy as np
'''This script focuses in doing the math for plotting the data we saved. It also can ignores TRACE28 because it is just
electronical noise, i.e., no light was applied for saving this particular data.'''

'''Read dictionary'''
pickle_in = open("1d_scan_5mm.pickle", "rb")
data5 = pickle.load(pickle_in)

# for k in range(27): #indenting this results in a later plot of the signal instead of plotting the gain
#     data5['TRACE' + str("{:02d}".format(k+1)) + '_gain'] = np.subtract(data5['TRACE' + str("{:02d}".format(k+1))][:, 1], data5['TRACE27'][:, 1])
for k in range(27):
    data5['TRACE' + str("{:02d}".format(k+1)) + '_gain'] = data5['TRACE' + str("{:02d}".format(k+1))][:, 1]

df_temp = np.zeros(shape=(350, 27))
for k in range(26):
    df_temp[:, k] = data5['TRACE' + str("{:02d}".format(k + 1)) + '_gain']
data5['TRACE_signal'] = df_temp

'''takes the gain at frequency 550 kHz for each height for plotting it later'''
df_temp = np.zeros(27)
for k in range(27):
    df_temp[k] = data5['TRACE' + str("{:02d}".format(k + 1)) + '_gain'][150]
data5['decay_5mm'] = np.array(df_temp).astype(np.float)

###########################################################################################################################################

'''SAVE DICTIONARY'''
pickle_out = open("1d_scan_5mm.pickle2", "wb")
pickle.dump(data5, pickle_out)
pickle_out.close()
###########################################################################################################################################

import numpy as np
import pickle

data = {}

pickle_in = open("2mmflux_close_1000to10000Hz.pickle", "rb")
data_close_1000to10000Hz = pickle.load(pickle_in)

pickle_in = open("2mmflux_far_1000to10000Hz.pickle", "rb")
data_far_1000to10000Hz = pickle.load(pickle_in)

sensitivity_close_1000to10000Hz = []
sensitivity_far_1000to10000Hz = []

for i in range(10):
    sensitivity_close_1000to10000Hz = np.append(sensitivity_close_1000to10000Hz,
                                                data_close_1000to10000Hz['Bmin' + str(i + 1)])
    sensitivity_far_1000to10000Hz = np.append(sensitivity_far_1000to10000Hz,
                                              data_far_1000to10000Hz['Bmin' + str(i + 1)])

data['sensitivity_close_1000to10000Hz'] = sensitivity_close_1000to10000Hz
data['sensitivity_far_1000to10000Hz'] = sensitivity_far_1000to10000Hz

pickle_out = open("sensitivity_1000to10000Hz.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()

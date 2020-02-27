import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

pickle_in = open("smoothed_data1.pickle", "rb")
data1 = pickle.load(pickle_in)

power = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]

f0 = np.where(np.isclose(data1['freq'], 10000, atol=10))
ff = np.where(np.isclose(data1['freq'], 1.00001e6, atol=10))
freq_index = (np.where((data1['freq'] >= f0) & (data1['freq'] <= ff)))
freq = data1['freq'][f0:ff]

coef_x_square = np.zeros(len(freq))
coef_x_lin = np.zeros(len(freq))

for k in freq_index:
    LPD_V_notdB = np.zeros(len(power))
    for i in range(len(power)):
        pickle_in = open("smoothed_data" + str(i+1) + ".pickle", "rb")
        data = pickle.load(pickle_in)

        LPD_V_notdB[i] = data['smooth_avg_FFT_scope_theo'][freq_index]

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
    coefs = poly.polyfit(power, LPD_V_notdB, 2)
    ffit = poly.Polynomial(coefs)
    # plt.plot(x_new, ffit(x_new))
    coef_x_square[k] = coefs[0]
    coef_x_lin[k] = coefs[1]


















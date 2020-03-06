import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

pickle_in = open("smoothed_data1(2).pickle", "rb")
data1 = pickle.load(pickle_in)

data1['freq'] = data1['freq'][160:16000]
data1['freq'] = data1['freq'][::10]

power = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]

coef_x_square = np.zeros(len(data1['freq']))
coef_x_lin = np.zeros(len(data1['freq']))

for k in range(len(data1['freq'])):
    LPD_V_notdB = np.zeros(len(power))
    for i in range(len(power)):
        pickle_in = open("smoothed_data" + str(i + 1) + "(2).pickle", "rb")
        data = pickle.load(pickle_in)

        data['smooth_avg_FFT_scope_theo'] = data['smooth_avg_FFT_scope_theo'][160:16000]
        data['smooth_avg_FFT_scope_theo'] = data['smooth_avg_FFT_scope_theo'][::10]

        LPD_V_notdB[i] = data['smooth_avg_FFT_scope_theo'][k]

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
    coefs = poly.polyfit(power, LPD_V_notdB, 2)
    ffit = poly.Polynomial(coefs)
    # plt.plot(x_new, ffit(x_new))
    coef_x_square[k] = coefs[2]
    coef_x_lin[k] = coefs[1]

ratio = coef_x_square/coef_x_lin

plt.figure(1)
plt.plot(data1['freq'], ratio)

plt.show()

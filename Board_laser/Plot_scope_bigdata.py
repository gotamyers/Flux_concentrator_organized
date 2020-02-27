import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# smoothed_data = {}

power = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
n_smooth = 300
freq_point = 50e3

pickle_in = open("dB_avg_FFT_scope_theo_0.pickle", "rb")
data0 = pickle.load(pickle_in)

freq = np.where(np.isclose(data0['freq'], freq_point))
LPD_V_notdB = np.zeros(len(power))
# smoothed_data['freq'] = data0['freq']

mask = data0['freq'] > 0
elec_noise = smooth(np.power(10, data0['dB_avg_FFT_scope_theo']/10), n_smooth)

for i in range(7):
    pickle_in = open("dB_avg_FFT_scope_theo_" + str(i + 1) + ".pickle", "rb")
    data_plot = pickle.load(pickle_in)

    '''Smoothing curve so that I can subtract electronical noise'''
    data_plot['smooth_dB_avg_FFT_scope_theo'] = smooth(np.power(10, data_plot['dB_avg_FFT_scope_theo']/10), n_smooth)
    data_plot['smooth_avg_FFT_scope_theo'] = np.abs(data_plot['smooth_dB_avg_FFT_scope_theo'] - elec_noise)
    data_plot['smooth_dB_avg_FFT_scope_theo'] = 10*np.log10(data_plot['smooth_avg_FFT_scope_theo'])
    # smoothed_data['smooth_avg_FFT_scope_theo'] = data_plot['smooth_avg_FFT_scope_theo']

    # ################################################################################################################
    # '''SAVE DICTIONARY'''
    # pickle_out = open("smoothed_data" + str(i + 1) + ".pickle", "wb")
    # pickle.dump(smoothed_data, pickle_out)
    # pickle_out.close()
    # ################################################################################################################

    LPD_V_notdB[i] = data_plot['smooth_avg_FFT_scope_theo'][freq]

    '''Plot test'''
    plt.figure(1)
    # plt.plot(data_plot['freq'][mask], data_plot['dB_avg_FFT_scope_theo'][mask])
    plt.plot(1e-3*data_plot['freq'][mask], data_plot['smooth_dB_avg_FFT_scope_theo'][mask], label=str(power[i]) + ' mW')


plt.xlim(9, 1e3)
plt.ylim(-150, -90)
plt.xlabel('Frequency (kHz)')
plt.ylabel('PSD')
plt.title('Laser photodetector')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

plt.figure(2)
plt.scatter(power, LPD_V_notdB)
plt.ylim(0, 5e-12)
plt.xlabel('Power (mW)')
plt.ylabel('Signal')

'''Fitting polynomial to figure (2)'''
x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
coefs = poly.polyfit(power, LPD_V_notdB, 1)
ffit = poly.Polynomial(coefs)
plt.plot(x_new, ffit(x_new))
print(coefs)

# pickle_in = open("dB_avg_FFT_noise.pickle", "rb")
# data_plot = pickle.load(pickle_in)
#
# mask = data_plot['freq'] > 0
#
# pickle_in = open("dB_avg_FFT_scope_theo_0.pickle", "rb")
# data1 = pickle.load(pickle_in)
#
#
# plt.figure(2)
# plt.plot(data_plot['freq'][mask], data_plot['dB_avg_FFT_scope_noise_theo'][mask], color='k')
# plt.plot(data_plot['freq'][mask], data1['dB_avg_FFT_scope_theo'][mask])
#
# plt.xlim(100e3, 0.2e6)
# plt.ylim(-150, -90)


plt.show()

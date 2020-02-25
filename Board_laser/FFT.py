import pickle
import numpy as np
import matplotlib.pyplot as plt

data_plot = {}
n_avg = 5      # number of averages

for i in range(8):
    pickle_in = open("scope_" + str(i) + ".pickle", "rb")
    data = pickle.load(pickle_in)

    N = len(data['scope_0'][:, 0])
    delta_t = data['scope_0'][1, 0] - data['scope_0'][0, 0]

    data['freq'] = np.fft.fftfreq(N, delta_t)
    mask = data['freq'] > 0


    '''F.T of the amplitude'''
    for k in range(5):
        data['FFT_scope_' + str(k)] = np.fft.fft(data['scope_' + str(k)][:, 1])
        data['FFT_scope_' + str(k) + '_theo'] = 2.0*(np.abs(data['FFT_scope_' + str(k)]/N))**2

    '''Averaging PSD'''
    soma = np.zeros(len(data['FFT_scope_0_theo']))
    for k in range(5):
        soma = soma + data['FFT_scope_' + str(k) + '_theo']
    data['avg_FFT_scope_theo'] = soma/n_avg

    data_plot['dB_avg_FFT_scope_theo'] = 10 * np.log10(data['avg_FFT_scope_theo'])
    data_plot['freq'] = data['freq']

    # ####################################################################################################################
    # '''SAVE DICTIONARY'''
    # pickle_out = open("dB_avg_FFT_scope_theo_" + str(i) + ".pickle", "wb")
    # pickle.dump(data_plot, pickle_out)
    # pickle_out.close()
    # ####################################################################################################################


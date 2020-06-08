import numpy as np
import matplotlib.pyplot as plt
import pickle
import numpy.polynomial.polynomial as poly
import scipy.optimize

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def parabola(x, a, b, c):
    return a*x**2 + b*x + c

data = {}
n_smooth = 70
power = [14.55, 20., 25., 30., 36.] #measured in mV (oscilloscope)
power = np.asarray(power)*2.0  #2 is because chao said the power is two times what was measured.16 is the offset in our case
power_w = np.asarray(power)/146.0

ref_data = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thMay2020\\testPSD024.bin", dtype='float', count=-1)
data["freq"] = ref_data[0] + ref_data[1]*np.array(range(len(ref_data[2:])))
data["shot_noise"] = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thMay2020\\testPSD024.bin", dtype='float', count=-1)[2:]
data["elec_noise"] = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thMay2020\\testPSD028.bin", dtype='float', count=-1)[2:]

data["smooth_dB_shot_noise"] = 10*np.log10(smooth(np.power(10, data["shot_noise"]/10), n_smooth))
data["smooth_dB_elec_noise"] = 10*np.log10(smooth(np.power(10, data["elec_noise"]/10), n_smooth))

for k in [13, 16, 17, 21, 22]:
    data["PSD_phase" + str(k)] = np.fromfile(
        "C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thMay2020\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

    data["smooth_PSD_phase" + str(k)] = smooth(np.power(10, data["PSD_phase" + str(k)]/10), n_smooth)
    data["smooth_dB_PSD_phase" + str(k)] = 10*np.log10(data["smooth_PSD_phase" + str(k)])

for k in [14, 15, 18, 19, 23]:
    data["PSD_amp" + str(k)] = np.fromfile(
        "C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\18thMay2020\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

    data["smooth_PSD_amp" + str(k)] = smooth(np.power(10, data["PSD_amp" + str(k)]/10), n_smooth)
    data["smooth_dB_PSD_amp" + str(k)] = 10*np.log10(data["smooth_PSD_amp" + str(k)])


'''fit coefficients for quantum and classical noise'''

coef_x_square_phase = np.zeros(len(data["freq"]))
coef_x_lin_phase = np.zeros(len(data["freq"]))
coef_x_constant_phase = np.zeros(len(data["freq"]))

for k in range(len(data['freq'])):
    LPD_V_notdB = np.zeros(len(power_w))
    a=0
    for i in [13, 16, 17, 21, 22]:
        LPD_V_notdB[a] = data["smooth_PSD_phase" + str(i)][k]
        a=a+1

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power_w[0], power_w[-1], num=len(power) * 50)
    coefs, pcov = scipy.optimize.curve_fit(parabola, power_w, LPD_V_notdB, bounds=(0, [1., 1., 1e-13]))
    # coefs = poly.polyfit(power, LPD_V_notdB, 2)
    # ffit = poly.Polynomial(coefs)
    coef_x_square_phase[k] = coefs[0]
    coef_x_lin_phase[k] = coefs[1]
    coef_x_constant_phase[k] = coefs[2]

ratio_phase = coef_x_square_phase/coef_x_lin_phase

coef_x_square_amp = np.zeros(len(data["freq"]))
coef_x_lin_amp = np.zeros(len(data["freq"]))
coef_x_constant_amp = np.zeros(len(data["freq"]))
for k in range(len(data['freq'])):
    LPD_V_notdB = np.zeros(len(power))
    a=0
    for i in [14, 15, 18, 19, 23]:
        LPD_V_notdB[a] = data["smooth_PSD_amp" + str(i)][k]
        a=a+1

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power_w[0], power_w[-1], num=len(power) * 50)
    coefs, pcov = scipy.optimize.curve_fit(parabola, power_w, LPD_V_notdB, bounds=(0, [1., 1., 1e-13]))
    coef_x_square_amp[k] = coefs[0]
    coef_x_lin_amp[k] = coefs[1]
    coef_x_constant_amp[k] = coefs[2]

ratio_amp = coef_x_square_amp/coef_x_lin_amp

data['coef_x_square_amp'] = coef_x_square_amp
data['coef_x_lin_amp'] = coef_x_lin_amp
data['coef_x_constant_amp'] = coef_x_constant_amp

data['coef_x_square_phase'] = coef_x_square_phase
data['coef_x_lin_phase'] = coef_x_lin_amp
data['coef_x_constant_phase'] = coef_x_constant_phase

########################################################################################################################
'''SAVE DICTIONARY'''
pickle_out = open("noise_board_laser.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
########################################################################################################################


# a = 0
# plt.figure(1)
# for k in [13, 16, 17, 21, 22]:
#     plt.plot(data["freq"], data["smooth_dB_PSD_phase" + str(k)], label=str(round(power_w[a], 2)) + " uW")
#     a = a+1
# plt.plot(data["freq"], data["smooth_dB_shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["smooth_dB_elec_noise"], label='elec_noise')
#
# plt.ylim(-150, -30)
# plt.xlim(1, 1e6)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Phase noise")
# plt.legend(loc='upper right')

# a=0
# plt.figure(2)
# for k in [14, 15, 18, 19, 23]:
#     plt.plot(data["freq"], data["smooth_dB_PSD_amp" + str(k)], label=str(round(power_w[a], 2)) + " uW")
#     a = a+1
# plt.plot(data["freq"], data["smooth_dB_shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["smooth_dB_elec_noise"], label='elec_noise')
#
# plt.ylim(-150, -30)
# plt.xlim(10, 100e3)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Amplitude noise")
# plt.legend(loc='upper right')

plt.figure(3)
plt.plot(data['freq'], coef_x_square_phase, label='square', color='red')
plt.plot(data['freq'], coef_x_lin_phase, label='linear', color='k')
plt.plot(data['freq'], coef_x_constant_phase, label='constant', color='blue')
# plt.plot(data['freq'], ratio_phase)

plt.xlim(1, 1e6)
# plt.ylim(-4e-9, 4e-9)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('1/mW')
plt.title("Phase noise coefficients")
plt.legend(loc='upper right')

plt.figure(4)
plt.plot(data['freq'], coef_x_square_amp, label='square', color='red')
plt.plot(data['freq'], coef_x_lin_amp, label='linear', color='k')
plt.plot(data['freq'], coef_x_constant_amp, label='constant', color='blue')
# plt.plot(data['freq'], ratio_amp)

plt.xlim(1, 1e6)
# plt.ylim(-2e-10, 2e-10)
plt.xscale('log')

plt.xlabel('Frequency (Hz)')
plt.ylabel('1/mW')
plt.title("Amplitude noise coefficients")
plt.legend(loc='upper right')

# plt.figure(5)
# plt.plot(data['freq'], coef_x_square_amp, label='amp', color='red')
# plt.plot(data['freq'], coef_x_square_phase, label='phase', color='k')
# # plt.plot(data['freq'], ratio_amp)
#
# plt.xlim(1, 1e6)
# plt.ylim(0, 5e-9)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('1/mW')
# plt.title("Square noise coefficients")
# plt.legend(loc='upper right')
#
# plt.figure(6)
# plt.plot(data['freq'], coef_x_lin_amp, label='amp', color='red')
# plt.plot(data['freq'], coef_x_lin_phase, label='phase', color='k')
# # plt.plot(data['freq'], ratio_amp)
#
# plt.xlim(1, 1e6)
# plt.ylim(-5e-11, 5e-10)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('1/mW')
# plt.title("Linear noise coefficients")
# plt.legend(loc='upper right')

# a = 0
# plt.figure(7)
# for k in [13, 16, 17, 21, 22]:
#     plt.plot(data["freq"], data["PSD_phase" + str(k)], label=str(round(power_w[a], 2)) + " uW")
#     a = a+1
# plt.plot(data["freq"], data["shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["elec_noise"], label='elec_noise')
#
# plt.ylim(-150, -30)
# plt.xlim(1, 1e6)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Phase noise")
# plt.legend(loc='upper right')

# a=0
# plt.figure(8)
# for k in [14, 15, 18, 19, 23]:
#     plt.plot(data["freq"], data["PSD_amp" + str(k)], label=str(round(power_w[a], 2)) + " uW")
#     a = a+1
# plt.plot(data["freq"], data["shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["elec_noise"], label='elec_noise')
#
# plt.ylim(-150, -30)
# plt.xlim(1, 1e6)
# plt.xscale('log')
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Amplitude noise")
# plt.legend(loc='upper right')

plt.show()

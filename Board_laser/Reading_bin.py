import numpy as np
import matplotlib.pyplot as plt
import pickle
import numpy.polynomial.polynomial as poly

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


data = {}
n_smooth = 100
power = [192, 152.8, 120, 91.4, 63.4, 33.27]

ref_data = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\9thApr2020\\testPSD020.bin", dtype='float', count=-1)
data["freq"] = ref_data[0] + ref_data[1]*np.array(range(len(ref_data[2:])))
data["shot_noise"] = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\9thApr2020\\testPSD020.bin", dtype='float', count=-1)[2:]
data["elec_noise"] = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\9thApr2020\\testPSD021.bin", dtype='float', count=-1)[2:]

data["smooth_dB_shot_noise"] = 10*np.log10(smooth(np.power(10, data["shot_noise"]/10), n_smooth))
data["smooth_dB_elec_noise"] = 10*np.log10(smooth(np.power(10, data["elec_noise"]/10), n_smooth))

for k in [6, 9, 11, 13, 15, 17]:
    data["PSD_phase" + str(k)] = np.fromfile(
        "C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\9thApr2020\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

    data["smooth_PSD_phase" + str(k)] = smooth(np.power(10, data["PSD_phase" + str(k)]/10), n_smooth)
    data["smooth_dB_PSD_phase" + str(k)] = 10*np.log10(data["smooth_PSD_phase" + str(k)])

for k in [7, 10, 12, 14, 16, 18]:
    data["PSD_amp" + str(k)] = np.fromfile(
        "C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\9thApr2020\\testPSD0{0}.bin".format(
            "{:02d}".format(k)), dtype='float', count=-1)[2:]

    data["smooth_PSD_amp" + str(k)] = smooth(np.power(10, data["PSD_amp" + str(k)]/10), n_smooth)
    data["smooth_dB_PSD_amp" + str(k)] = 10*np.log10(data["smooth_PSD_amp" + str(k)])

########################################################################################################################
'''SAVE DICTIONARY'''
# pickle_out = open("phase_amp_noise_board_laser.pickle", "wb")
# pickle.dump(data, pickle_out)
# pickle_out.close()
########################################################################################################################
'''fit coefficients for quantum and classical noise'''

coef_x_square_phase = np.zeros(len(data["freq"]))
coef_x_lin_phase = np.zeros(len(data["freq"]))

for k in range(len(data['freq'])):
    LPD_V_notdB = np.zeros(len(power))
    a=0
    for i in [6, 9, 11, 13, 15, 17]:
        LPD_V_notdB[a] = data["smooth_PSD_phase" + str(i)][k]
        a=a+1

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
    coefs = poly.polyfit(power, LPD_V_notdB, 2)
    ffit = poly.Polynomial(coefs)
    # plt.plot(x_new, ffit(x_new))
    coef_x_square_phase[k] = coefs[2]
    coef_x_lin_phase[k] = coefs[1]

ratio_phase = coef_x_square_phase/coef_x_lin_phase

coef_x_square_amp = np.zeros(len(data["freq"]))
coef_x_lin_amp = np.zeros(len(data["freq"]))
for k in range(len(data['freq'])):
    LPD_V_notdB = np.zeros(len(power))
    a=0
    for i in [7, 10, 12, 14, 16, 18]:
        LPD_V_notdB[a] = data["smooth_PSD_amp" + str(i)][k]
        a=a+1

    '''Fitting polynomial to figure (2)'''
    x_new = np.linspace(power[0], power[-1], num=len(power) * 10)
    coefs = poly.polyfit(power, LPD_V_notdB, 2)
    ffit = poly.Polynomial(coefs)
    # plt.plot(x_new, ffit(x_new))
    coef_x_square_amp[k] = coefs[2]
    coef_x_lin_amp[k] = coefs[1]

ratio_amp = coef_x_square_amp/coef_x_lin_amp


# a = 0
# plt.figure(1)
# for k in [6, 9, 11, 13, 15, 17]:
#     plt.plot(data["freq"], data["smooth_dB_PSD_phase" + str(k)], label=str(power[a]))
#     a = a+1
# plt.plot(data["freq"], data["smooth_dB_shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["smooth_dB_elec_noise"], label='elec_noise')
#
# plt.xlim(0, 2e5)
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Phase noise")
# plt.legend(loc='upper right')
#
# a=0
# plt.figure(2)
# for k in [7, 10, 12, 14, 16, 18]:
#     plt.plot(data["freq"], data["smooth_dB_PSD_amp" + str(k)], label=str(power[a]))
#     a = a+1
# plt.plot(data["freq"], data["smooth_dB_shot_noise"], label='shot_noise')
# plt.plot(data["freq"], data["smooth_dB_elec_noise"], label='elec_noise')
#
# plt.xlim(0, 2e5)
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.title("Amplitude noise")
# plt.legend(loc='upper right')
#
plt.figure(3)
plt.plot(data['freq'], coef_x_square_phase, label='square', color='b')
plt.plot(data['freq'], coef_x_lin_phase, label='linear', color='red')
# plt.plot(data['freq'], ratio_phase)

plt.xlim(0, 2e5)
plt.ylim(0, 1e-11)

plt.xlabel('Frequency (Hz)')
plt.ylabel('1/mW')
plt.title("Phase noise coefficients")
plt.legend(loc='upper right')

plt.figure(4)
plt.plot(data['freq'], coef_x_square_amp, label='square', color='b')
plt.plot(data['freq'], coef_x_lin_amp, label='linear', color='red')
# plt.plot(data['freq'], ratio_amp)

plt.xlim(0, 2e5)
plt.ylim(0, 1e-11)

plt.xlabel('Frequency (Hz)')
plt.ylabel('1/mW')
plt.title("Amplitude noise coefficients")
plt.legend(loc='upper right')


plt.show()

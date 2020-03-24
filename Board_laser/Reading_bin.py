import numpy as np
import matplotlib.pyplot as plt

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


n_smooth = 10

# data = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD001.bin", dtype='float', count=-1)
# PSD1 = data[2:]
# PSD2 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD002.bin", dtype='float', count=-1)[2:]
# PSD3 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD003.bin", dtype='float', count=-1)[2:]
# PSD4 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD004.bin", dtype='float', count=-1)[2:]

data = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\21thMar2020\\testPSD001.bin", dtype='float', count=-1)
PSD1 = data[2:]
PSD2 = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\21thMar2020\\testPSD002.bin", dtype='float', count=-1)[2:]
PSD3 = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\21thMar2020\\testPSD003.bin", dtype='float', count=-1)[2:]
PSD4 = np.fromfile("C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Board_laser\\21thMar2020\\testPSD004.bin", dtype='float', count=-1)[2:]

f0 = data[0]
df = data[1]
freq = f0 + df*np.array(range(len(PSD1)))

# PSD1_not_dB = smooth(np.power(10, PSD1/10), n_smooth)
# PSD2_not_dB = smooth(np.power(10, PSD2/10), n_smooth)
# PSD3_not_dB = smooth(np.power(10, PSD3/10), n_smooth)
# PSD4_not_dB = smooth(np.power(10, PSD4/10), n_smooth)
#
# PSD1_not_dB = PSD1_not_dB - PSD4_not_dB
# PSD2_not_dB = PSD2_not_dB - PSD4_not_dB
# PSD3_not_dB = PSD3_not_dB - PSD4_not_dB
#
# PSD1 = 10*np.log10(PSD1_not_dB)
# PSD2 = 10*np.log10(PSD2_not_dB)
# PSD3 = 10*np.log10(PSD3_not_dB)
# PSD4 = 10*np.log10(PSD4_not_dB)

plt.plot(freq, PSD1, color='blue')
plt.plot(freq, PSD2, color='red')
plt.plot(freq, PSD3, color='k')
plt.plot(freq, PSD4, color='olive')
plt.xlim(0, 2e4)

plt.show()

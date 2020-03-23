import numpy as np
import matplotlib.pyplot as plt

PSD1 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD001.bin", dtype='float', count=-1)
PSD2 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD002.bin", dtype='float', count=-1)
PSD3 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD003.bin", dtype='float', count=-1)
PSD4 = np.fromfile("C:\\Users\\Fernando\\Documents\\Phd\\Board_laser\\21thMarch2020\\testPSD004.bin", dtype='float', count=-1)

freq = np.linspace(1, len(PSD1), len(PSD1))

PSD1_not_dB = np.power(10, PSD1/10)
PSD2_not_dB = np.power(10, PSD2/10)
PSD3_not_dB = np.power(10, PSD3/10)
PSD4_not_dB = np.power(10, PSD4/10)


plt.plot(freq, PSD1)
plt.plot(freq, PSD2)
plt.plot(freq, PSD3)
plt.plot(freq, PSD4)

plt.show()
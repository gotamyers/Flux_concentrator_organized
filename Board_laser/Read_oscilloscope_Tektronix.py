import pyvisa
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

rm = pyvisa.ResourceManager()
rm.list_resources()
scope = rm.open_resource('USB0::0x0699::0x0413::C011694::INSTR') #need to look at the usb port it is connected to the scope

data = {}

scope.write('DATA:SOU CH3')
scope.write('DATA:WIDTH 1')
scope.write('DATA:ENC RPB')

ymult = float(scope.ask('WFMPRE:YMUL?'))
yzero = float(scope.ask('WFMPRE:YZERO?'))
yoff = float(scope.ask('WFMPRE:YOFF?'))
xincr = float(scope.ask('WFMPRE:XINCR?'))

scope.write('CURVE?')
data = scope.read_raw()
headerlen = 2 + int(data[1])
header = data[:headerlen]
ADC_wave = data[headerlen:-1]

ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

Volts = (ADC_wave - yoff) * ymult + yzero

Time = np.arange(0, xincr * len(Volts), xincr)

N = len(Time)
delta_t = Time[1] - Time[0]

freq = np.fft.fftfreq(N, delta_t)
mask = freq > 0

voltz_Hz = np.fft.fft(Volts)
PSD = 20.0 * np.log10(2.0 * np.abs(voltz_Hz / N))

averages = 5

if averages > 1:
    for k in range(averages):
        scope.write('CURVE?')
        data = scope.read_raw()
        headerlen = 2 + int(data[1])
        header = data[:headerlen]
        ADC_wave = data[headerlen:-1]

        ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

        Volts = (ADC_wave - yoff)*ymult + yzero

        Time = np.arange(0, xincr*len(Volts), xincr)

        N = len(Time)
        delta_t = Time[1] - Time[0]

        freq = np.fft.fftfreq(N, delta_t)
        mask = freq > 0

        voltz_Hz = np.fft.fft(Volts)
        PSD = PSD + 20.0*np.log10(2.0*np.abs(voltz_Hz/N))

        #plt.plot(Time, Volts)

        plt.plot(freq[mask],  PSD[mask])

        plt.pause(1)



else:
    plt.figure(1, figsize=(15, 6), dpi=100)
    plt.plot(Time, Volts)

    plt.figure(2, figsize=(15, 6), dpi=100)
    plt.plot(freq[mask], PSD[mask])

    plt.show()


plt.tight_layout()
plt.show()

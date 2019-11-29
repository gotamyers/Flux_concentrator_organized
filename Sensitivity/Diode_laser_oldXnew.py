import math
import pickle
import numpy as np
import matplotlib.pyplot as plt

'''This script is for comparing continuous data obtained with NA and compare with quantized data from SA'''

pickle_in = open("sensitivity_2mm.pickle", "rb")
continuous_data = pickle.load(pickle_in)

pickle_in = open("2and5flux_SA_funcgen_10to1000khz.pickle", "rb")
quantized_data = pickle.load(pickle_in)

mu0 = 4 * math.pi * 1e-7  # Magnetic permeability vacuum
Ncoils = 10  # Number of turns
dwire = 0.8  # Wires thickness
radius = 0.03  # Coil radius
R = 50  # Resistance (ohms)
L = 2 * mu0 * radius * Ncoils * (np.log10(16 * radius / dwire) - 2)  # Inductance
frequencies = np.asarray([10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 200, 300, 400, 500, 600, 700, 800, 900, 990])
noise_frequencies = [10, 20, 45, 70, 110, 200, 300, 500, 800]
power_in = 2
V_drive = 10/(2*math.sqrt(2))  # Voltagem driven to the coil
RBW = 30  # Resolution bandwidth
I_driven = np.divide(V_drive, np.sqrt(R**2 + (1000*frequencies * 2 * np.pi)**2*L**2))  # Coils current
B_ref = pow(4.5, 1.5) * mu0 * Ncoils * I_driven / radius
letters = ['a', 'b', 'c']

########################################################################################################################
for k in frequencies:
    for i in letters:
        quantized_data['S21_' + i + str(k)] = 28 + 10*np.log10(np.multiply(quantized_data['SNRV' + i + str(k)],
                                                                         quantized_data['noise_maxV' + i + str(k)])/power_in)


########################################################################################################################
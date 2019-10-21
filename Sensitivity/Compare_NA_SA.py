import csv
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt


'''This script is for comparing continuous data obtained with NA and compare with quantized data from SA'''

pickle_in = open("simple_sensitivity_2mm.pickle", "rb")
cont_data = pickle.load(pickle_in)

pickle_in = open("2mmflux_SA_funcgen_10to1000khz.pickle", "rb")
quantized_data = pickle.load(pickle_in)



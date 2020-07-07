import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

all = pd.read_excel('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Papers\\SurveyFG.xlsx', header=None)
commercial_mag = all.iloc[23:, :]


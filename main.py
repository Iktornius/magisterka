import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal._savitzky_golay import savgol_filter as sgf
def conv(x):
    return x.replace(',', '.').encode('utf-8')

read = np.genfromtxt((conv(x) for x in open('13G-mapa-0009.CSV')), delimiter=';')

pre_x = read[:,0]
x = np.flip(pre_x[pre_x>250]) # wave number, cm-1, area below 250 is overshadowed due to Rayleigh scattering
y = read[:len(x),1] # Raman intensity, no unit

smooth_y = sgf(y, 31, 2)

plt.plot(x, smooth_y, linewidth=2)
plt.plot(x, y, color='red', linewidth=0.75)

axis = ('Wave number [1/cm]', 'Raman intensity')
plt.xlabel(axis[0])
plt.ylabel(axis[1])
plt.show()




import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from matplotlib import pyplot as plt
from scipy.signal._savitzky_golay import savgol_filter as sgf
from scipy.signal import peak_widths
import peakutils as pku

### FUNCTIONS ###

def conv(x):
    return x.replace(',', '.').encode('utf-8')

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# "Asymmetric Least Squares Smoothing" by P. Eilers and H. Boelens, 2005
def baseline_als(y, lam, p, niter=10):
  L = len(y)
  D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
  w = np.ones(L)
  for i in range(niter):
    W = sparse.spdiags(w, 0, L, L)
    Z = W + lam * D.dot(D.transpose())
    z = spsolve(Z, w*y)
    w = p * (y > z) + (1-p) * (y < z)
  return z

#################

read = np.genfromtxt((conv(x) for x in open('13G-mapa-0009.CSV')), delimiter=';')

pre_x = read[:,0]


x = pre_x[pre_x>250] # wave number, cm-1, area below 250 is overshadowed due to Rayleigh scattering
y = read[len(pre_x)-len(x):,1] # Raman intensity, no unit

smooth_y = sgf(y, 15, 2)
bline = baseline_als(smooth_y, 10**7, 0.001)
blinecut_y = smooth_y - bline


peaks = pku.indexes(blinecut_y, thres=0.1, min_dist=30)

#get 960 peak
phosphate_tonormalize_x = find_nearest(x[peaks], 960)
phosphate_tonormalize_y = blinecut_y[peaks][np.where(phosphate_tonormalize_x==x[peaks])]

#plt.scatter(phosphate_tonormalize_x, phosphate_tonormalize_y, color='green')

#plt.plot(x, blinecut_y, linewidth=2)
norm_y = blinecut_y/phosphate_tonormalize_y
norm_peaks = pku.indexes(norm_y, thres=0.1, min_dist=30)

phosphate_x = find_nearest(x[norm_peaks], 960)
phosphate_y = norm_y[norm_peaks][np.where(phosphate_x==x[norm_peaks])]

carbonate_x = find_nearest(x[norm_peaks], 1070)
carbonate_y = norm_y[norm_peaks][np.where(carbonate_x==x[norm_peaks])]

amide_x = find_nearest(x[norm_peaks], 1670)
amide_y = norm_y[norm_peaks][np.where(amide_x==x[norm_peaks])]


plt.scatter(phosphate_x, phosphate_y, color='green')
plt.scatter(carbonate_x, carbonate_y, color='green')
plt.scatter(amide_x, amide_y, color='green')

plt.plot(x, norm_y, color='red')
#plt.plot(x, y, color='red', linewidth=0.75)

axis = ('Wave number [1/cm]', 'Raman intensity')
plt.xlabel(axis[0])
plt.ylabel(axis[1])
plt.xlim(max(x),min(x))

#### RESULTS ####
mineralization = (phosphate_y/amide_y)[0]
substitution = carbonate_x/phosphate_x
fwhm = peak_widths(norm_y, np.where(phosphate_y==norm_y)[0], rel_height=0.5)[0][0]
crystallinity = 1/fwhm

print('### RESULTS ###')
print('Mineralization: {}\nSubstitution: {}\nPhosphate band FWHM: {}\nCrystallinity: {}\n'.format(mineralization, substitution, fwhm, crystallinity))




plt.show()

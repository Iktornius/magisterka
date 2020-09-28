import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from matplotlib import pyplot as plt
from scipy.signal._savitzky_golay import savgol_filter as sgf
from scipy.signal import peak_widths, argrelextrema
import peakutils as pku

### FUNCTIONS ###

def get_data():
    #csv = input('CSV Filename: ')
    csv = '13G-mapa-0009.csv'
    file = open(csv)
    delimiter = file.readline()[13]

    if file.readline().count(',')>1:
        read = np.genfromtxt((conv(x) for x in file), delimiter=delimiter)
    else:
        read = np.genfromtxt((x for x in file), delimiter=delimiter)

    pre_x = read[:, 0]
    x = pre_x[pre_x > 250]  # wave number, cm-1, area below 250 is overshadowed due to Rayleigh scattering
    y = read[len(pre_x) - len(x):, 1]  # Raman intensity, no unit
    file.close()
    return x, y

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


def peak_cords(peaks, band, x, y):
    peak_x = find_nearest(x[peaks], band)
    peak_y = y[peaks][np.where(peak_x==x[peaks])]
    return peak_x, peak_y

def init_prep():
    x, y = get_data()
    smooth_y = sgf(y, 15, 2)
    bline = baseline_als(smooth_y, 10 ** 7, 0.001)
    blinecut_y = smooth_y - bline
    return x, blinecut_y

def get_surface(compound, threshold, color):
    comp_x = compound[0]
    comp_ind = np.where(x==comp_x)
    print(comp_ind)
    minimas = argrelextrema(norm_y, np.less)[0]
    nearest = find_nearest(minimas, comp_ind)

    ind = np.where(minimas == nearest)[0][0]
    if nearest>comp_ind:
        scope = (ind-threshold, ind+(threshold-1))
    else:
        scope = (ind-(threshold+1), ind+threshold)

    diff = np.diff(x)
    dx = sum(diff)/len(diff)
    plt.fill_between(x[minimas[scope[0]]:minimas[scope[-1]]], norm_y[minimas[scope[0]]:minimas[scope[-1]]], color=color)
    area = np.trapz(norm_y[minimas[scope[0]]:minimas[scope[-1]]], dx=dx)
    return area



def find_desired():
    peaks = pku.indexes(blinecut_y, thres=0.1, min_dist=30)
    # get 960 peak
    phosphate_tonormalize_x, phopshate_tonormalize_y = peak_cords(peaks, 960, x, blinecut_y)
    norm_y = blinecut_y / phopshate_tonormalize_y
    norm_peaks = pku.indexes(norm_y, thres=0.2, min_dist=30)
    phosphate_x, phosphate_y = peak_cords(norm_peaks, 960, x, norm_y)
    carbonate_x, carbonate_y = peak_cords(norm_peaks, 1070, x, norm_y)
    amide_x, amide_y = peak_cords(norm_peaks, 1670, x, norm_y)
    phosphate = (phosphate_x, phosphate_y)
    carbonate = (carbonate_x, carbonate_y)
    amide = (amide_x, amide_y)
    return phosphate, carbonate, amide, norm_y




def get_plot():
    plt.scatter(phosphate[0], phosphate[1], color='green', label='Phosphate band')
    plt.scatter(carbonate[0], carbonate[1], color='black', label='Carbonate band')
    plt.scatter(amide[0], amide[1], color='blue', label='Amide band')
    plt.plot(x, norm_y, color='red')
    axis = ('Wave number [1/cm]', 'Raman intensity')
    plt.xlabel(axis[0])
    plt.ylabel(axis[1])
    plt.xlim(max(x), min(x))
    plt.legend()
    plt.show()

def results():
    #### RESULTS ####
    mineralization = (phosphate[1] / amide[1])[0]
    substitution = (carbonate[1] / phosphate[1])[0]
    fwhm = peak_widths(norm_y, np.where(phosphate[1] == norm_y)[0], rel_height=0.5)[0][0]
    crystallinity = 1 / fwhm
    print('### RESULTS ###')
    print('Mineralization: {}\nSubstitution: {}\nPhosphate band FWHM: {}\nCrystallinity: {}\n'.format(mineralization,
                                                                                                      substitution,
                                                                                                      fwhm,
                                                                                                      crystallinity))

def main():
    global phosphate, carbonate, amide, norm_y, x, blinecut_y
    x, blinecut_y = init_prep()
    phosphate, carbonate, amide, norm_y = find_desired()
    get_surface(phosphate, 1, 'green')
    get_plot()
    results()




if __name__=='__main__':
    main()
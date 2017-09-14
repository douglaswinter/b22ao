import numpy as np
from math import ceil, floor


def generate_gaussian_target(beam, fwhm=5e-3, intensity_filter=0.25, centre=None):
    """If target is not provided, will capture image,
    and generate a gaussian with specified FWHM"""

    x = np.arange(0, beam.shape[1], 1, float)
    y = np.arange(0, beam.shape[0], 1, float)
    y = y[:, np.newaxis]

    if not centre:
        y0, x0 = find_centre(beam, intensity_filter)
    else:
        y0, x0 = centre

    return np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)


def find_centre(img, intensity_filter):
    """
    Martin Stancsics's answer to
    stackoverflow.com/questions/37519238/python-find-centre-of-object-in-an-image
    :param img: in matrix notation i, j
    :return: i0, j0
    """
    hi = normalise_and_filter(img, intensity_filter)
    hi = hi / np.sum(np.sum(hi))

    # marginal distributions
    di = np.sum(hi, 1)
    dj = np.sum(hi, 0)

    # expected values
    i0 = np.sum(di * np.arange(img.shape[0]))
    j0 = np.sum(dj * np.arange(img.shape[1]))
    return make_integer(i0), make_integer(j0)


def make_integer(num):
    if num % floor(num) < 0.5:
        return floor(num)
    else:
        return ceil(num)


def normalise_and_filter(img, intensity_filter):
    max_intensity = np.max(img)
    min_intensity = np.min(img)
    normalised = img.copy()
    hi = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            normalised[i, j] = (img[i, j] - min_intensity) / (max_intensity - min_intensity)
            hi[i, j] = normalised[i, j] > intensity_filter

    return hi


def normalise(img):
    max_intensity = np.max(img)
    min_intensity = np.min(img)
    normalised = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            normalised[i, j] = (img[i, j] - min_intensity) / (max_intensity - min_intensity)
    return normalised

def load_wct(path):
    import pandas as pd

    img = pd.read_csv(path, skiprows=5, header=None)
    img = pd.DataFrame.as_matrix(img)
    img = np.reshape(img, ([479, 640]))
    target = np.ones([480, 640])
    target[:-1, :] = img
    return target

def plot_figures(*args):
    from matplotlib import pyplot as plt
    for arg in args:
        plt.figure()
        plt.imshow(arg)
        
    plt.show()
import numpy as np
import SPGDutils
import random
from matplotlib import pyplot as plt


def six_part_beam():
    beam = np.zeros([10,10])

    hi = 10
    mid = 8

    hiIndeces = [[3,3],[3,6],
                 [5,3],[5,6],
                 [7,3],[7,6]]

    midIndeces = [[2,3],[2,6],
                  [3,2],[3,4],[3,5],[3,7],
                  [4,3],[4,6],
                  [5,2],[5,4],[5,5],[5,7],
                  [6,3],[6,6],
                  [7,2],[7,4],[7,5],[7,7],
                  [8,3],[8,6]]

    for point in range(len(hiIndeces)):
        i, j = hiIndeces[point]
        beam[i,j] = hi

    for point in range(len(midIndeces)):
        i, j = midIndeces[point]
        beam[i,j] = mid

    return beam


def random_beam(size=([480, 640]), spots=6):
    beam = np.zeros(size)

    for spot in range(spots):
        centre = [random.randint(0, size[0]), random.randint(0, size[1])]
        beam += SPGDutils.generate_gaussian_target(beam, 100, 0, centre)
    return beam

def target_from_file(path):

    import pandas as pd
    import numpy as np

    img = pd.read_csv(path, skiprows=5, header=None)
    img = pd.DataFrame.as_matrix(img)
    img = np.reshape(img, ([479, 640]))
    target = np.ones([480, 640])
    target[:-1, :] = img
    return target

# beam = random_beam(spots=4)
# beam = six_part_beam()
beam = target_from_file("target.wct")

# gaussian FWHM
pixel_size = 17e-6
target_size = 1e-3
fwhm = target_size/pixel_size

target = SPGDutils.generate_gaussian_target(beam, fwhm, 0.25)

plt.figure()
plt.imshow(beam)
plt.title("beam")

plt.figure()
plt.imshow(target)
plt.title("generated target")

plt.show()


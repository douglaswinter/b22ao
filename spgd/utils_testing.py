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
        individual_gauss = SPGDutils.generate_gaussian_target(beam, 20, 0, centre)
        beam += individual_gauss
    return beam

beam = random_beam(spots=2)
# beam = six_part_beam()

pixel_size = 17e-6
target_size = 1e-3


target = SPGDutils.generate_gaussian_target(beam, target_size/pixel_size, 0.25)
# target = SPGDutils.generate_gaussian_target(beam, 3, 0.25)

plt.figure()
plt.imshow(beam)
plt.title("beam")

plt.figure()
plt.imshow(target)
plt.title("generated target")

plt.show()


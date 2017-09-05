from math import sqrt
import numpy as np


class DMSim:
    '''
    *very* simple deformable mirror simulation
    contraints:
        numAct must be the square of a number
    '''

    def __init__(self, numAct):
        self.numAct = numAct

        self.pixels = [Actuator() for index in range(numAct)]

    def deform(self, signal):
        '''
        :param signal: voltages 0-1
        :return:
        '''
        assert (signal.shape[0] == self.numAct)

        for index in range(self.numAct):
            self.pixels[index].setValue(signal[index])

    def getPositions(self):
        return [self.pixels[index].value for index in range(self.numAct)]

    '''
    for this simulation, input is same size as mirror
    i.e. sqrt(numAct) by sqrt(numAct)

    the input pixel corresponding to that actuator
    will 'move' depending on the actuator voltage 
    '''

    def reflect(self, img):
        sqrSide = int(sqrt(self.numAct))
        out = np.zeros([sqrSide, sqrSide])

        for i in range(sqrSide):
            for j in range(sqrSide):
                out = out + self.influence(img + out, i, j)

        return out / self.numAct

    def influence(self, original, i, j):
        length = original.shape[0]
        gap = 1 / 8

        v = float(self.pixels[i * int(sqrt(self.numAct)) + j].value)
        pixel = original[i, j]
        img = np.zeros(original.shape)
        if v > 0:
            img[i, j] = 0

        if v < gap:
            # move pixel N
            if i - 1 >= 0:
                img[i - 1, j] = pixel
        elif v < 2 * gap:
            # move pixel NE
            if i - 1 >= 0 and j + 1 < length:
                img[i - 1, j + 1] = pixel
        elif v < 3 * gap:
            # move pixel E
            if j + 1 < length:
                img[i, j + 1] = pixel
        elif v < 4 * gap:
            # move pixel SE
            if i + 1 < length and j + 1 < length:
                img[i + 1, j + 1] = pixel
        elif v < 5 * gap:
            # move pixel S
            if i + 1 < length:
                img[i + 1, j] = pixel
        elif v < 6 * gap:
            # move pixel SW
            if i + 1 < length and j - 1 >= 0:
                img[i + 1, j - 1] = pixel
        elif v < 7 * gap:
            # move pixel W
            if j - 1 >= 0:
                img[i, j - 1] = pixel
        else:
            # move pixel NW
            if i - 1 >= 0 and j - 1 >= 0:
                img[i - 1, j - 1] = pixel

        return img

    def simpleMultiply(self, img):
        side = int(sqrt(self.numAct))
        v = np.array(self.getPositions()).reshape(side, side)
        return v * img


class Actuator:
    def __init__(self):
        self.value = 0

    def setValue(self, value):
        self.value = value
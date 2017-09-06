from dm_cam.dm_cam_operation import DMCamOperation
import numpy


class SumOfInfluence(DMCamOperation):
    def __init__(self):
        DMCamOperation.__init__(self, "Test")

    def run(self):
        import time
        img = numpy.zeros([640, 480])
        for i in range(97):
            self.deform(poke_pixel(i))
            time.sleep(0.2)
            img += self.capture()

        show_image(img, "Sum of influence functions")


def poke_pixel(number):
    signal = numpy.zeros(97)
    signal[number]=1
    return signal


def show_image(img, title=""):
    from matplotlib import pyplot as plt
    plt.figure()
    plt.imshow(img)
    plt.title(title)
    plt.show()
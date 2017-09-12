import sys, os
sys.path.insert(0, os.path.abspath('..'))
# Integrated DM and WinCamD system for custom operations
from dm_cam.dm_cam_runner import DMCamRunner
from dm_cam.dm_cam_operation import DMCamOperation


import struct

''' Add '/Lib' or '/Lib64' to path '''

if (8 * struct.calcsize("P")) == 32:
    print("Use x86 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib'))
else:
    print("Use x86_64 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib64'))
    
    
import numpy as np
from matplotlib import pyplot as plt
    
class GenerateSuitableTarget(DMCamOperation):
    def __init__(self):
        DMCamOperation.__init__(self, label="Generate target")
        self.intensity_filter = 0.25
    def run(self):

        clear = np.zeros([97,])
        self.deform(clear)
        
        img = self.capture()
        
        
        centre = self.find_centre(img)
        target = self.generate_gaussian_target(centre=centre)
        
        plt.figure()
        plt.imshow(img)
        plt.title("captured image")
        
        plt.figure()
        plt.imshow(target)
        plt.title("suggested target")
        plt.show()
        
        
    def find_centre(self, img):
        """
        Martin Stancsics's answer to
        stackoverflow.com/questions/37519238/python-find-centre-of-object-in-an-image
        :param img:
        :return: cx, cy
        """
        hi = self.normalise_and_filter(img)
        hi = hi / np.sum(np.sum(hi))

        # marginal distributions
        dx = np.sum(hi, 0)
        dy = np.sum(hi, 1)

        # expected values
        cx = np.sum(dx * np.arange(img.shape[0]))
        cy = np.sum(dy * np.arange(img.shape[1]))

        return self.make_integer(cx), self.make_integer(cy)
    
    def normalise_and_filter(self, img):
        max_intensity = np.max(img)
        min_intensity = np.min(img)
        normalised = img
        hi = np.zeros(img.shape)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                normalised[i, j] = (img[i, j] - min_intensity) / (max_intensity - min_intensity)
                hi[i, j] = normalised[i, j] > self.intensity_filter

        return hi
    
    def make_integer(self, num):
        from math import floor, ceil
        if num % floor(num) < 0.5:
            return floor(num)
        else:
            return ceil(num)
    
    
    def generate_gaussian_target(size=([480, 640]), fwhm=20, centre=None):
        import numpy as np
        x = np.arange(0, size[0], 1, float)
        y = np.arange(0, size[1], 1, float)
        y = y[:, np.newaxis]
    
        if centre is None:
            x0 = size[0] // 2
            y0 = size[1] // 2
        else:
            x0 = centre[0]
            y0 = centre[1]
    
        return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)
    
    
if __name__ == "__main__":
    app = DMCamRunner(mirror_serial="BAX112", title="Finding an SPGD target")
    app.set_operation(GenerateSuitableTarget())
    app.MainLoop()
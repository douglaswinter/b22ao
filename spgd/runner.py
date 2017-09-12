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
    
# parameters for SPGD algorithm
target = "C:\\Users\\Public\\Documents\\Python Scripts\\b22ao\\spgd\\target.wct"
num_act = 97
maxV = 1
minV = -1
convergence_criterion = 1e-6
max_iterations = 15
gamma = -0.1
intensity_filter = 0.25


def target_from_file(path):
    import pandas as pd
    import numpy as np

    img = pd.read_csv(path, skiprows=5, header=None)
    img = pd.DataFrame.as_matrix(img)
    img = np.reshape(img, ([479, 640]))
    target = np.array([480, 640])
    target[0:480, :]=img
    target[480, :] = np.ones([1,640])
    return target


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


class WinCamDALPAOSPGD(DMCamOperation):
    def __init__(self, target):
        from SPGD import SPGD
        DMCamOperation.__init__(self, label="SPGD")

        # initiate spgd object
        self.spgd = SPGD(self,
                         num_act=num_act,
                         max_v=maxV,
                         min_v=minV,
                         target=target,
                         convergence_criterion=convergence_criterion,
                         max_iterations=max_iterations,
                         gamma=gamma,
                         intensity_filter=intensity_filter,
                         debug=True
                         )

    def run(self):
        self.spgd.optimise_with_target()


if __name__ == "__main__":
    app = DMCamRunner(mirror_serial="BAX112", title="SPGD optimization of deformable mirror")
    app.set_operation(WinCamDALPAOSPGD(target_from_file(target)))
    app.MainLoop()

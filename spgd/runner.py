# Integrated DM and WinCamD system for custom operations
from dm_cam_runner import DMCamRunner
from dm_cam_operation import DMCamOperation

# parameters for SPGD algorithm
target_path = "C:\\Users\\blah"
num_act = 97
maxV = 1
minV = -1
convergence_criterion = 1e-6
max_iterations = 5000
gamma = -0.1
intensity_filter = 0.25


def target_from_file(path):
    import pandas as pd
    import numpy as np

    img = pd.read_csv(path, skiprows=5, header=None)
    img = pd.DataFrame.as_matrix(img)
    return np.reshape(img, ([479, 640]))


class WinCamDALPAOSPGD(DMCamOperation):
    def __init__(self, target):
        from SPGD import SPGD
        DMCamOperation.__init__(self, label="SPGD")

        # initiate spgd object
        self.spgd = SPGD(self,
                         num_act,
                         maxV,
                         minV,
                         target,
                         convergence_criterion,
                         max_iterations,
                         gamma,
                         intensity_filter
                         )

    def run(self):
        self.spgd.optimise_with_target()


if __name__ == "__main__":
    app = DMCamRunner(mirror_serial="BAX112", title="SPGD optimization of deformable mirror")
    app.set_operation(WinCamDALPAOSPGD(target_from_file(target_path)))
    app.MainLoop()

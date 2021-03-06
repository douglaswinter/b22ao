import sys, os
sys.path.insert(0, os.path.abspath('..'))
# Integrated DM and WinCamD system for custom operations
from dm_cam.dm_cam_runner import DMCamRunner
from dm_cam.dm_cam_operation import DMCamOperation

    
# parameters for SPGD algorithm
target = "C:\\Users\\Public\\Documents\\Python Scripts\\b22ao\\spgd\\target.wct"
num_act = 97
maxV = 1
minV = -1
convergence_criterion = 1e-6
max_iterations = 2000
gamma = -1000
intensity_filter = 0


class WinCamDALPAOSPGD(DMCamOperation):
    def __init__(self, target=None):
            
        DMCamOperation.__init__(self, label="SPGD", burn=True)
        
        self.target = target

    def run(self):
        from SPGD import SPGD
        import SPGDutils
        import numpy as np

        if not self.target:
            print("Target not specified, will generate from camera capture")
            width = 2e-3 // 17e-6
            img = self.capture()
            # norm = SPGDutils.normalise(img)
            # SPGDutils.plot_figures(img, norm)
            self.target = SPGDutils.generate_gaussian_target(img, width, 0.1, None)
            
            SPGDutils.plot_figures(img, self.target)
            np.savetxt("original.csv", img, delimiter=",")

        # initiate spgd object
        self.spgd = SPGD(self,
                         num_act=num_act,
                         max_v=maxV,
                         min_v=minV,
                         target=self.target,
                         convergence_criterion=convergence_criterion,
                         max_iterations=max_iterations,
                         gamma=gamma,
                         intensity_filter=intensity_filter,
                         debug=True
                         )

        control = self.spgd.optimise_with_target()
        np.savetxt("mirror_command.csv", control, delimiter=",")
        

if __name__ == "__main__":
    mirror_serial = "BAX111"

    app = DMCamRunner(mirror_serial=mirror_serial, title="SPGD optimization of deformable mirror")
    app.set_operation(WinCamDALPAOSPGD())
    app.MainLoop()

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
max_iterations = 30
gamma = -10
intensity_filter = 0.45


class WinCamDALPAOSPGD(DMCamOperation):
    def __init__(self, target=None):
            
        DMCamOperation.__init__(self, label="SPGD", burn=True)
        
        self.target = target

    def run(self):
        import SPGDutils
        from SPGD import SPGD
        
        import numpy as np
        import numpy.ma as ma
        if not self.target:
            print("Target not specified, will generate from camera capture")
            width = 1e-3 // 17e-6
            img = self.capture()
            
            print(np.max(img))
            print(img.min())
#            np.savetxt("RAW.csv", img, delimiter=",")
#            normimg = (img-img.min())/(img.max()-img.min())
#            
##            masked = ma.array(img, mask=[img<1], fill_value=10)
##            img = masked.filled()
#            self.target = SPGDutils.generate_gaussian_target(img, 100, 0.25)
#            
#            error = 0
#
#            for i in range(img.shape[0]):
#                for j in range(img.shape[1]):
#                    error += (img[i, j] - self.target[i, j])**2
#            print(error)
#            
#            SPGDutils.plot_figures(img, normimg, self.target)
#            
#            SPGDutils.plot_figures(np.loadtxt("RAW.csv", delimiter=","))
            

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
        # self.spgd.optimise_with_target()
#        print("initial error:")
#        signal = self.spgd.initialise_control_signal()
#        print(self.spgd.difference_with_target(signal))
#        
#        delta_u = self.spgd.gen_perturbation()
#        jum = self.spgd.difference_with_target(signal-delta_u)
#        jup = self.spgd.difference_with_target(signal+delta_u)
#        print("Delta J = " + str(jup-jum))


if __name__ == "__main__":
    mirror_serial = "BAX111"

    app = DMCamRunner(mirror_serial=mirror_serial, title="SPGD optimization of deformable mirror")
    app.set_operation(WinCamDALPAOSPGD())
    app.MainLoop()

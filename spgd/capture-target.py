import sys, os
sys.path.insert(0, os.path.abspath('..'))
# Integrated DM and WinCamD system for custom operations
from dm_cam.dm_cam_runner import DMCamRunner
from dm_cam.dm_cam_operation import DMCamOperation
import csv

import struct

''' Add '/Lib' or '/Lib64' to path '''

if (8 * struct.calcsize("P")) == 32:
    print("Use x86 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib'))
else:
    print("Use x86_64 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib64'))
    
class ImageTarget(DMCamOperation):
    def __init__(self):
        DMCamOperation.__init__(self, label="Capture")
         
    def run(self):
        import numpy
        self.deform(numpy.zeros(97,))
        img = self.capture()
        filename = "C:\\Users\\Public\\Documents\\target.csv"
        with open(filename, 'wb') as fp:
            w = csv.writer(fp, delimiter=',')
            w.writerows(img)
            
        print("Done")
        
         

if __name__ == "__main__":
    app= DMCamRunner(mirror_serial="BAX111")
    app.set_operation(ImageTarget())
    app.MainLoop()
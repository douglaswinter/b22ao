import sys, os
sys.path.insert(0, os.path.abspath('..'))
from dm_cam.dm_cam_runner import DMCamRunner
from live_testing.operations import SumOfInfluence

import sys
import os
#import time
import struct

''' Add '/Lib' or '/Lib64' to path '''

if (8 * struct.calcsize("P")) == 32:
    print("Use x86 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib'))
else:
    print("Use x86_64 libraries.")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib64'))
    
    
''' Import Alpao SDK class '''
from asdk import DM

serial = "BAX111"
app = DMCamRunner(serial, title="Sum of influence functions")
app.set_operation(SumOfInfluence())
app.MainLoop()

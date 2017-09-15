# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 09:31:17 2016

@author: snf56384
"""

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

dm1 = DM( "BAX111" )
dm2 = DM( "BAX112" )


#dm1.Send( check1on2 )
#dm2.Send( -Zplot )

dm1.Reset()
dm2.Reset()

#import numpy as np
#
#signal = np.loadtxt("mirror_command_1.csv", delimiter=",")
#dm1.Send(signal)


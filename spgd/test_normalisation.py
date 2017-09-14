import numpy as np

a=np.loadtxt("RAW.csv", delimiter=",")
print(a.max())
print(a.min())
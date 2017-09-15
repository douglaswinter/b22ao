from SPGDutils import *

a=np.loadtxt("RAW.csv", delimiter=",")
plot_figures(a, normalise(abs(a)))
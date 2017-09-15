from SPGDutils import *

# r = np.zeros([10, 10])
# gauss = generate_gaussian_target(r, fwhm=3, centre=([5, 5]))

# plot_figures(gauss, flatten(gauss, 0.7))

r = abs(np.loadtxt("RAW.csv", delimiter=","))

gauss = generate_gaussian_target(r, intensity_filter=0.01)

plot_figures(r, gauss)

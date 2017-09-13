import numpy as np


def target_from_file(path):

    import pandas as pd

    img = pd.read_csv(path, skiprows=5, header=None)
    img = pd.DataFrame.as_matrix(img)
    img = np.reshape(img, ([479, 640]))
    target = np.ones([480, 640])
    target[:-1, :] = img
    return target

def plot_figures(*args):
    from matplotlib import pyplot as plt
    for arg in args:
        plt.figure()
        plt.imshow(arg)
        
    plt.show()
    
beam = target_from_file("target.wct")

burn = beam.copy()
burn[200:400, 280:400] = 1
    
corrected = beam-burn

plot_figures(beam, burn, corrected)


np.savetxt("burned_pixels.csv", burn, delimiter=",")

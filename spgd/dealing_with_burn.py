from SPGDutils import *

original_target = load_wct("target.wct")
burn = load_wct("burn_only.wct")

width = 1e-3 // 17e-6  # target width

# raw = np.loadtxt("raw_capture.csv", delimiter=",")  # already subtracted


def subtracting():

    raw = original_target-burn

    raw[raw < 0] = 0  # background is 0; where burn was is < 0

    normalised = normalise(raw)

    target = generate_gaussian_target(normalised, width, 0.25, centre=None)

    plot_figures(original_target, raw, normalised, target, normalised - target)

    print(calculate_error(normalised, target))


def masking():
    import numpy.ma as ma
    masked = ma.array(original_target, mask=[burn>1])
    target = generate_gaussian_target(masked, width)
    plot_figures(masked, target)
    print(calculate_error(masked, target))


def calculate_error(img, target):
    pixel_errors=[]
    error = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel_error = (img[i, j] - target[i, j])**2
            pixel_errors.append(pixel_error)
            error += pixel_error
    print("total error = " + str(error))
    print("max pixel error = "+str(max(pixel_errors)))

    return error

# masking()  # not working yet

subtracting()



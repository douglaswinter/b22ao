from SPGDutils import *

original_target = load_wct("target.wct")
burn = load_wct("burn_only.wct")

width = 1e-3 // 17e-6  # target width

# raw = np.loadtxt("raw_capture.csv", delimiter=",")  # already subtracted

plot = False


def subtracting():

    raw = original_target-burn
    raw[raw < 0] = 0  # background is 0; where burn was is < 0
    normalised = normalise(raw)
    target = generate_gaussian_target(normalised, width, 0.25, centre=None)
    if plot:
        plot_figures(original_target, raw, normalised, target, normalised - target)
    error = calculate_error(normalised, target)
    return error


def masking():
    import numpy.ma as ma
    masked = ma.array(original_target, mask=[burn > 1], fill_value=1)
    corrected = normalise(masked.filled())
    target = generate_gaussian_target(corrected, width)
    if plot:
        plot_figures(corrected, target)
    error = calculate_error(corrected, target)
    return error


def calculate_error(img, target):
    pixel_errors = []
    error = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel_error = (img[i, j] - target[i, j])**2
            pixel_errors.append(pixel_error)
            error += pixel_error

    return error

e_mask = masking()

e_sub = subtracting()

print("Subtracting: " + str(e_sub))
print("Masking: " + str(e_mask))

import SPGDutils
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt


class SPGD:

    def __init__(self, ao_wrapper, num_act, min_v, max_v, target=None,
                 convergence_criterion=1.42, max_iterations=5000, gamma=-0.1,
                 intensity_filter=0.25, debug=False, plot=True):
        """
        Implementation of stochastic parallel gradient descent algorithm
        to optimise beam profile using deformable mirror

        Algorithm principle followed from :
            Song, Yang, et al. "Optimization of Stochastic Parallel Gradient Descent Algorithm
            via Power Spectrum Method." Applied Mathematics & Information Sciences 10.1 (2016): 325.

        :param ao_wrapper: object which implements the method deform_and_capture(signal)
        :param num_act: number of actuators
        :param min_v: minimum voltage to apply to individual actuator
        :param max_v: maximum voltage to apply to individual actuator
        :param target: for optimise_with_target()
        :param convergence_criterion: convergence_criterion
        :param max_iterations:
        :param gamma: negative to minimise performance metric, positive to maximise
        :param intensity_filter: normalised intensities below this value are filtered out
        :param debug: for verbose output
        :param plot: plots results
        """
        self.ao_wrapper = ao_wrapper
        self.num_act = num_act
        self.min_v = min_v
        self.max_v = max_v
        self.convergence_criterion = convergence_criterion
        self.gamma = gamma
        self.debug = debug
        self.target = target
        self.max_iterations = max_iterations
        self.intensity_filter = intensity_filter
        self.plot = plot

    '''
    run the algorithm
    '''
    def optimise_with_target(self):
        """
        Run SPGD algorithm minimising error between actual image and target image

        J = Sum_x( Sum_y( [ I_actual(x,y) - I_target(x,y) ]^2 ) )
        """
        if self.target is None:
            print("Target not set; will try to optimise anyway...")
            return self.optimise_with_centre()

        return self.optimize(self.difference_with_target)

    '''
    run the algorithm
    '''
    def optimise_with_centre(self):
        return self.optimize(self.biggest_distance_from_centre)

    def optimize(self, strategy):
        control_signal = self.initialise_control_signal()
        metric = strategy(control_signal)
        print("ignore the following")
        iteration = 0
        metric_history = []
        while metric > self.convergence_criterion and iteration < self.max_iterations:
            delta_u = self.gen_perturbation()
            u_plus = control_signal + delta_u
            u_minus = control_signal - delta_u
            j_u_plus = strategy(u_plus)
            j_u_minus = strategy(u_minus)
            delta_j = j_u_plus - j_u_minus
            control_signal = control_signal + self.gamma * delta_u * delta_j
            metric = strategy(control_signal)
            metric_history.append(metric)
            if self.debug:
                print("iteration number %d" % iteration)
                print("J = %f" % metric)
                print(control_signal[:4])
            iteration += 1

        if self.plot:
            print("***************\nFinished after " + str(iteration) + " iterations\n")
            print("Control vector:")
            print(control_signal)
            print("J = " + str(metric))
            img = self.ao_wrapper.deform_and_capture(control_signal)
            self.plot_results(img, metric_history)

        return control_signal

    def plot_results(self, img, js):

        # target
        if self.target is not None:
            plt.figure()
            plt.imshow(self.target)
            plt.title("target")

        # with final control vector
        plt.figure()
        plt.imshow(img)
        plt.title("with final control vector")

        plt.figure()
        x = np.arange(0, len(js))
        plt.plot(x, js)
        plt.title("convergence")

        plt.show()

    def initialise_control_signal(self):
        start = self.min_v + (self.max_v - self.min_v) / 2
        return np.ones(self.num_act)*start

    def gen_perturbation(self):
        amplitude = 0.2
        sigmas = [-amplitude, amplitude]
        return np.random.choice(sigmas, self.num_act)

    def difference_with_target(self, signal):

        img = self.ao_wrapper.deform_and_capture(signal)
        np.savetxt("raw_capture.csv", img, delimiter=",")
        img = SPGDutils.normalise_and_filter(img, 0)
        np.savetxt("normalised_capture.csv", img, delimiter=",")
        error = 0

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                error += (img[i, j] - self.target[i, j])**2
        return error

    def biggest_distance_from_centre(self, signal):

        img = self.ao_wrapper.deform_and_capture(signal)

        centre = SPGDutils.find_centre(img, self.intensity_filter)

        distance = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j] != 0:
                    distance = max(distance, sqrt((i-centre[0])**2 + (j-centre[1])**2))

        return distance
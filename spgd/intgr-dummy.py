from math import sqrt
import numpy as np
from dummy import ddm
from dummy.DummyObjects import DummyNonGuiRunner, DMCamOperation


def target_spot(beam):
    target = np.zeros(beam.shape)
    for i in range(4, 6):
        for j in range(4, 6):
            target[i, j] = 1
    return target


def generate_beam(num, points=10):

    if num==100:
        beam = np.zeros([10,10])

        hi = 10
        mid = 8

        hiIndeces = [[3,3],[3,6],
                     [5,3],[5,6],
                     [7,3],[7,6]]

        midIndeces = [[2,3],[2,6],
                      [3,2],[3,4],[3,5],[3,7],
                      [4,3],[4,6],
                      [5,2],[5,4],[5,5],[5,7],
                      [6,3],[6,6],
                      [7,2],[7,4],[7,5],[7,7],
                      [8,3],[8,6]]

        for point in range(len(hiIndeces)):
            i, j = hiIndeces[point]
            beam[i,j] = hi

        for point in range(len(midIndeces)):
            i, j = midIndeces[point]
            beam[i,j] = mid
    else:
        square = int(sqrt(num))
        beam = np.zeros([square, square])

        for point in range(points):
            i, j = np.random.randint(0, square, 2)
            beam[i, j] = 1

    return beam


class DummyWrapper:
    def __init__(self, mirror, beam):
        self.mirror = mirror
        self.beam = beam

    def deform_and_capture(self, signal):
        self.mirror.deform(signal)
        return self.mirror.reflect(self.beam)


class DummySPGD(DMCamOperation):
    def __init__(self, target, mirror, beam):
        from SPGD import SPGD
        DMCamOperation.__init__(self)
        self.alg = SPGD(ao_wrapper=DummyWrapper(mirror, beam),
                          num_act=num_actuators,
                          target=target,
                          max_v=1,
                          min_v=-1,
                          intensity_filter=0.2,
                          max_iterations=2000,
                          convergence_criterion=0.01,
                          gamma=-0.05,
                          debug=True,
                          plot=True)

    def run(self):
        self.alg.optimise_with_target()


if __name__ == '__main__':
    num_actuators = 100
    mirror = ddm.DMSim(num_actuators)
    beam = generate_beam(num_actuators)
    target = target_spot(beam)

    app = DummyNonGuiRunner(mirror)
    app.set_operation(DummySPGD(target, mirror, beam))
    app.button_pressed()


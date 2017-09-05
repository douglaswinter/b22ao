import numpy
from soapy import confParse, SCI, atmosphere, DM
from SPGD import SPGD

# setup soapy conf
conf_path = "conf/sim.yaml"
conf = confParse.loadSoapyConfig(conf_path)

# setup atmospheric distortion
atmos = atmosphere.atmos(conf)
dist = atmos.randomScrns()

# setup simulations DM
dm = DM.Piezo(conf)
n_acts = dm.getActiveActs()

# initiate control object
control = numpy.zeros((conf.sim.nDM, conf.sim.scrnSize, conf.sim.scrnSize))

# setup camera
cam = SCI.PSF(conf)

# light with no correction
beam = cam.frame(dist[0]).copy()

# target
target = cam.frame(None).copy()


# system wrapper
class SystemWrapper:
    def __init__(self, configuration, mirror, camera, distortion):
        self.configuration = configuration
        self.mirror = mirror
        self.camera = camera
        self.distortion = distortion

    def _deform(self, signal):
        return self.mirror.dmFrame(signal)

    def _snapshot(self, correction):
        return self.camera.frame(self.distortion[0], correction).copy()

    def deform_and_capture(self, signal):
        """
        Moves DM and captures snapshot
        :param signal: to send to DM. 1d array, of size dm.getActiveActs()
        :return: corrected image, of size self.conf.sim.scrnSize ** 2
        """
        dm_correction = numpy.zeros((self.configuration.sim.nDM, self.configuration.sim.scrnSize, self.configuration.sim.scrnSize))
        dm_correction[0] = self._deform(signal)
        return self._snapshot(dm_correction)

ao_wrapper = SystemWrapper(conf, dm, cam, dist)


# these parameters worked for target strategy
spgd = SPGD(ao_wrapper=ao_wrapper,
            debug=False,
            num_act=n_acts,
            min_v=-1,
            max_v=1,
            target=target,
            convergence_criterion=0.01,
            intensity_filter=0.4,
            gamma=-100,
            max_iterations=5000
            )

spgd.optimise_with_target()

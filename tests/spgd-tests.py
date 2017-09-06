import unittest

from SPGD import SPGD


class SPGDTests(unittest.TestCase):

    def deform_and_capture(self, signal):
        """this method will allow me to use 'self' as ao_wrapper"""
        import numpy
        return numpy.ones([450, 450])

    def test_safe_defaults(self):
        a = self.init_spgd
        # hooray, no errors!

    def test_difference_with_target(self):
        # captured image and target equal, error should be zero
        target = self.deform_and_capture(None)  # signal is inconsequential
        spgd = self.init_spgd(target)
        error = spgd.difference_with_target(None)

        self.assertEqual(0, error)

        # modify target
        target[5:10, 1] = 0
        spgd = self.init_spgd(target)
        error1 = spgd.difference_with_target(None)

        # modify target further
        target[5, 6:8] = 0
        spgd = self.init_spgd(target)
        error2 = spgd.difference_with_target(None)

        self.assertGreater(error2, error1)

    def test_output_control(self):
        import numpy
        spgd = self.init_spgd(self.deform_and_capture(None))
        output_control = spgd.optimise_with_target()
        # because target and captured are equal...
        self.assertTrue(numpy.all(numpy.zeros(97)==output_control))

    def init_spgd(self, target=None):
        return SPGD(ao_wrapper=self,
                         num_act=97,
                         min_v=-1,
                         max_v=1,
                         plot=False,
                         target=target) # everything else is default
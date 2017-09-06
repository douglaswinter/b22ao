from threading import Thread
import numpy


class DMCamOperation(Thread):
    """
    Base class for WinCamD and DM operations.

    Provides the methods self.deform(signal) and self.capture(),
    as well as the compound method self.deform_and_capture(signal)

    """
    def __init__(self, label="Custom operation"):
        """
        :param label: (Optional) will become the button text
        """
        Thread.__init__(self)

        # for readability:
        self.camera = None
        self.mirror = None
        self.label = label

    def run(self):
        """
        Child classes must override this method
        """
        print("Concrete operation needs to override run()!")

    def set_camera(self, camera):
        """
        This method is called by DMCamRunner, getting the camera object through activeX
        :param camera:
        """
        import time

        self.camera = camera
        self.camera.ctrl.StartDriver()
        time.sleep(5)
        self.camera.ctrl.StartDevice()
        time.sleep(1)

    def set_mirror(self, mirror):
        """
        This method is called by DMCamRunner
        :param mirror: ALPAO DM object
        """
        self.mirror = mirror

    def deform(self, signal):
        """
        Send control signal to mirror
        :param signal: numpy array of size 97
        """
        if self.mirror:
            self.mirror.Send(signal)
        else:
            print("Mirror has not been set.")

    def get_label(self):
        """
        Called by DMCamRunner.
        Can be overridden to set DMCamRunner's button text
        :return: Button label (string)
        """
        return self.label

    def capture(self):
        """
        Camera snapshot
        :return: 640 x 480 array
        """
        data = self.camera.ctrl.GetWinCamDataAsVariant()
        data = [[x] for x in data]
        return numpy.reshape(data, [640, 480])

    def deform_and_capture(self, signal):
        """Send signal to mirror, wait 200 ms, then image it"""
        import time
        self.deform(signal)
        time.sleep(0.2)
        return self.capture()

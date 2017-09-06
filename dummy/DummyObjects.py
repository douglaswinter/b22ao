import numpy
from dm_cam.dm_cam_operation import DMCamOperation


class DummyNonGuiRunner:
    def __init__(self, mirror, title="Dummy runner"):

        self.camera = DummyCamera()
        self.operation_thread = None
        self.mirror = mirror

    def set_operation(self, operation):
        self.operation_thread = operation
        self.operation_thread.set_camera(self.camera)
        self.operation_thread.set_mirror(self.mirror)

    def button_pressed(self):
        if self.operation_thread is not None:
            self.operation_thread.start()
        else:
            print("Operation not set")

class DummyCamera:
    def __init__(self):

        self.ctrl = DummyCtrl()


class DummyCtrl:
    def GetWinCamDataAsVariant(self):
        print("Capturing snapshot")
        return numpy.random.rand(640*480)

    def StartDriver(self):
        print("Driver started")

    def StartDevice(self):
        print("Device started")

class DummyMirror:
    def Send(self, signal):
        print("Moving mirror; signal:")
        print(signal)


class DummyOperation(DMCamOperation):

    def __init__(self, label):
        DMCamOperation.__init__(self)
        self.label = label

    def get_label(self):
        return self.label

    def run(self):
        print("Running some stuff...")
        self.deform(numpy.random.rand(5))
        print(self.capture())

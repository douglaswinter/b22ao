# imports for GUI
import wx
#import wx.lib.activex

from dummy.DummyObjects import DummyCamera
import copy


class DummyGuiRunner(wx.App):

    def __init__(self, redirect=False, filename=None, title='Python Interface to DataRay'):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY, size=(310, 130), title=title)

        self.camera = DummyCamera()
        self.mirror = None

        # Button Panel
        bp = wx.Panel(parent=self.frame, id=wx.ID_ANY, size=(300, 100))

        # Custom controls
        self.button = wx.Button(bp, label="", pos=(0, 0), size=(300, 100))
        self.button.Bind(wx.EVT_BUTTON, self.button_pressed)

        # Worker thread
        self.operation = None
        self.operation_thread = None

        self.frame.Show()

    def set_mirror(self, mirror):
        self.mirror = mirror

    def set_operation(self, operation):
        self.button.SetLabel(operation.get_label())
        self.operation = operation

    def configure_devices(self):
        self.operation_thread.set_camera(self.camera)
        self.operation_thread.set_mirror(self.mirror)

    def button_pressed(self, event):
        if not self.operation_thread:
            if not self.operation:
                print("Operation not set")
            else:
                self.operation_thread = copy.copy(self.operation)
                self.configure_devices()
                self.operation_thread.start()
                self.operation_thread = None
        else:
            print("Operation already running")

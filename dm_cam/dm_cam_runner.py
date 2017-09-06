# imports for GUI
import wx
import wx.lib.activex
import comtypes.client


class EventSink(object):

    def __init__(self, frame):
        self.counter = 0
        self.frame = frame

    def DataReady(self):
        self.counter += 1
        self.frame.Title = "DataReady fired {0} times".format(self.counter)


class DMCamRunner(wx.App):
    def __init__(self, mirror_serial=None, redirect=False, filename=None, title='Python Interface to DataRay'):
        """
        Object to initialise WinCamD through activeX and (optionally) an ALPAO deformable mirror
        and perform a custom operation on a separate thread.

        Operation must be implemented as a subclass of DMCamOperation, and set using DMCamRunner.set_operation(operation)

        :param mirror_serial: e.g. "BAX112"
        :param title: A title for the GUI window
        """
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY,size=(760,500), title=title)

        # Panel
        p = wx.Panel(self.frame, wx.ID_ANY)

        # Start camera
        self.camera = wx.lib.activex.ActiveXCtrl(p, 'DATARAYOCX.GetDataCtrl.1')

        self.counter = 0
        sink = EventSink(self.frame)
        self.sink = comtypes.client.GetEvents(self.gd.ctrl, sink)

        # Button Panel
        bp = wx.Panel(parent=self.frame, id=wx.ID_ANY, size=(215, 250))
        b1 = wx.lib.activex.ActiveXCtrl(parent=bp, size=(200, 50), pos=(7, 0), axID='DATARAYOCX.ButtonCtrl.1')
        b1.ctrl.ButtonID = 297  # Id's for some ActiveX controls must be set
        b2 = wx.lib.activex.ActiveXCtrl(parent=bp, size=(100, 25), pos=(5, 55), axID='DATARAYOCX.ButtonCtrl.1')
        b2.ctrl.ButtonID = 171
        b3 = wx.lib.activex.ActiveXCtrl(parent=bp, size=(100, 25), pos=(110, 55), axID='DATARAYOCX.ButtonCtrl.1')
        b3.ctrl.ButtonID = 172
        b4 = wx.lib.activex.ActiveXCtrl(parent=bp, size=(100, 25), pos=(5, 85), axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID = 177
        b4 = wx.lib.activex.ActiveXCtrl(parent=bp, size=(100, 25), pos=(110, 85), axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID = 179

        # Custom controls
        t = wx.StaticText(bp, label="File:", pos=(5, 115))
        self.ti = wx.TextCtrl(bp, value="C:\\Users\\Public\\Documents\\output.csv", pos=(30, 115), size=(170, -1))
        self.rb = wx.RadioBox(bp, label="Data:", pos=(5, 140), choices=["Profile", "WinCam"])
        self.cb = wx.ComboBox(bp, pos=(5, 200), choices=["Profile_X", "Profile_Y", "Both"])
        self.cb.SetSelection(0)
        self.button = wx.Button(bp, label="", pos=(100, 225))
        self.button.Bind(wx.EVT_BUTTON, self.button_pressed)

        # Pictures
        pic = wx.lib.activex.ActiveXCtrl(parent=self.frame, size=(250, 250), axID='DATARAYOCX.CCDimageCtrl.1')
        tpic = wx.lib.activex.ActiveXCtrl(parent=self.frame, size=(250, 250), axID='DATARAYOCX.ThreeDviewCtrl.1')
        palette = wx.lib.activex.ActiveXCtrl(parent=self.frame, size=(10, 250), axID='DATARAYOCX.PaletteBarCtrl.1')

        # Profiles
        self.px = wx.lib.activex.ActiveXCtrl(parent=self.frame, size=(300, 200), axID='DATARAYOCX.ProfilesCtrl.1')
        self.px.ctrl.MyID = 22
        self.py = wx.lib.activex.ActiveXCtrl(parent=self.frame, size=(300, 200), axID='DATARAYOCX.ProfilesCtrl.1')
        self.py.ctrl.MyID = 23

        # Formatting
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(item=bp, flag=wx.RIGHT, border=10)
        row1.Add(pic)
        row1.Add(item=tpic, flag=wx.LEFT, border=10)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(self.px, 0, wx.RIGHT, 100)  # Arguments: item, proportion, flags, border
        row2.Add(self.py)
        col1 = wx.BoxSizer(wx.VERTICAL)
        col1.Add(item=row1, flag=wx.BOTTOM, border=10)
        col1.Add(item=row2, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.frame.SetSizer(col1)

        # Initialise mirror if provided
        self.mirror = self.init_mirror(mirror_serial)

        # Worker thread
        self.operation_thread = None

        self.frame.Show()

    def set_operation(self, operation):
        """
        Set the function to run (on a separate thread) on pressing the button

        :param operation: subclass of DMCamOperation
        """
        self.button.SetLabel(operation.label())
        self.operation_thread = operation
        self.operation_thread.set_camera(self.camera)
        self.operation_thread.set_mirror(self.mirror)

    def button_pressed(self):
        if self.operation_thread is not None:
            self.operation_thread.begin()
        else:
            print("Operation not set")


def init_mirror(serial):
    if serial:
        import sys
        import os
        import struct
        if (8 * struct.calcsize("P")) == 32:
            print("Use x86 libraries.")
            sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib'))
        else:
            print("use x86_64 libraries.")
            sys.path.append(os.path.join(os.path.dirname(__file__), 'Lib64'))

        from asdk import DM

        return DM(serial)
    else:
        print("WARNING: no mirror serial provided")
        return None

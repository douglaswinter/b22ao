from dm_cam.dm_cam_runner import DMCamRunner
from live_testing.operations import SumOfInfluence

serial = "BAX112"
app = DMCamRunner(serial, title="Sum of influence functions")
app.set_operation(SumOfInfluence())
app.MainLoop()

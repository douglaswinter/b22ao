from dummy.DummyGuiRunner import DummyGuiRunner
from dummy.DummyObjects import *
from live_testing.operations import SumOfInfluence

app = DummyGuiRunner(DummyMirror(), title="Sum of influence functions")
app.set_operation(SumOfInfluence())
app.MainLoop()

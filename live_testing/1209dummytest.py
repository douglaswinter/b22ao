import sys, os
sys.path.insert(0, os.path.abspath('..'))
from dummy.DummyGuiRunner import DummyGuiRunner
from dummy.DummyObjects import *
from live_testing.operations import SumOfInfluence

app = DummyGuiRunner(DummyMirror(), title="Sum of influence functions")
app.set_operation(SumOfInfluence())
app.MainLoop()

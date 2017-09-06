from DummyGuiRunner import DummyGuiRunner
from dummy.DummyObjects import DummyOperation, DummyMirror

if __name__ == '__main__':
    app = DummyGuiRunner()
    app.set_mirror(DummyMirror())
    app.set_operation(DummyOperation("Dummy operation"))
    app.MainLoop()

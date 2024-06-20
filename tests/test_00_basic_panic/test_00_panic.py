import pytest

from basic_panic import Panic, PanicHandler, panic, SystemPanicHandler


def test_panic():
    with pytest.raises(Panic) as exc_info:
        panic("Something went wrong")
    assert str(exc_info.value) == "Something went wrong"
    assert repr(exc_info.value) == "Panic(message='Something went wrong', code=1)"


def test_panic_handler():

    # -- TEST: if on_panic is not implemented in a subclass of PanicHandler

    class CustomPanicHandler2(PanicHandler):

        def on_panic(self, panic: Panic) -> None:
            super().on_panic(panic)

    with pytest.raises(NotImplementedError):
        with CustomPanicHandler2():
            panic("Something went wrong")

    # -- TEST: if on_panic is implemented in a subclass of PanicHandler

    class CustomPanicHandler(PanicHandler):

        def on_panic(self, panic: Panic) -> None:
            print("Panic caught:", panic)
            assert str(panic) == "Something went wrong"

    with CustomPanicHandler():
        with pytest.raises(Panic) as exc_info:
            panic("Something went wrong")
        assert str(exc_info.value) == "Something went wrong"


def test_system_panic_handler(capfd):

    with pytest.raises(SystemExit) as exc_info:
        with SystemPanicHandler():
            panic("Something went wrong")

        assert exc_info.value.code == 1
        assert capfd.readouterr().out == "PANIC [Errno 1]: Something went wrong\n"

import pytest

from basic_panic import Panic, PanicHandler, panic


def test_panic():
    with pytest.raises(Panic) as exc_info:
        panic("Something went wrong")
    assert str(exc_info.value) == "Something went wrong"

    class CustomPanicHandler(PanicHandler):

        def on_panic(self, panic: Panic) -> None:
            print("Panic caught:", panic)
            assert str(panic) == "Something went wrong"

    with CustomPanicHandler():
        with pytest.raises(Panic) as exc_info:
            panic("Something went wrong")
        assert str(exc_info.value) == "Something went wrong"
    # Panic caught: Something went wrong

# -- STL Imports --
from abc import ABC, abstractmethod
from dataclasses import dataclass
import sys
from types import TracebackType
# from typing import override # Python 3.12 feature, enable when available


@dataclass
class Panic(Exception):
    """
    A panic is a runtime error that is not expected to be recovered from. It is used to indicate
    that the program is in an unrecoverable state and should be terminated. Panics can be caught
    using a PanicHandler context manager and should only be caught on the top level of the program.
    As a general rule try to avoid catching broad BaseExceptions or Exceptions. Also avoid using
    unspecific except clauses, as they can have unintended side effects (like catching Panics).

    Inheritance:
        Exception

    Attributes:
        message (str): The message to be displayed when the panic is raised.
        code (int): The exit code to be returned when the panic is raised. Default is 1.

    Example::

        >>> raise Panic("Something went wrong")
        Panic: Something went wrong
    """
    message: str
    code: int = 1

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"Panic(message={self.message!r}, code={self.code})"


def panic(message: str, code: int = 1):
    """
    Raises a Panic with the given message and code.

    Args:
        message (str): The message to be displayed when the panic is raised.
        code (int): The exit code to be returned when the panic is raised. Default is 1.

    Example::

        >>> panic("Something went wrong")
        Panic: Something went wrong
    """
    raise Panic(message, code)


class PanicHandler(ABC):
    """
    A context manager that catches panics and allows for custom handling.

    Example::

        >>> class CustomPanicHandler(PanicHandler):
        ...     def on_panic(self, panic: Panic) -> None:
        ...         print("Panic caught:", panic)
        ...
        >>> with CustomPanicHandler():
        ...     panic("Something went wrong")
        ...
        Panic caught: Something went wrong
    """

    def __enter__(self) -> None:
        """
        Enters the context manager.
        """

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """
        Exits the context manager.

        Args:
            exc_type (type[BaseException] | None): The type of the exception raised.
            exc_val (BaseException | None): The exception raised.
            exc_tb (TracebackType | None): The traceback of the exception raised.

        Returns:
            bool: True if the exception was handled, False otherwise.
        """
        if isinstance(exc_val, Panic):
            self.on_panic(exc_val)

        return True

    @abstractmethod
    def on_panic(self, p: Panic) -> None:
        """
        Abstract method to be implemented by subclasses. Called when a panic is raised.

        Args:
            p (Panic): The panic that was raised.
        """
        raise NotImplementedError


class SystemPanicHandler(PanicHandler):
    """
    A context manager that catches panics and prints them to stderr.

    Example::

        >>> with SystemPanicHandler():
        ...     panic("Something went wrong")
        ...
        PANIC [Errno 1]: Something went wrong
    """

    # @override   # Python 3.12 feature, enable when available
    def on_panic(self, p: Panic) -> None:
        print(f"PANIC [Errno {p.code}]:", p.message, file = sys.stderr)
        sys.exit(p.code)

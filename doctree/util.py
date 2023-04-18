from __future__ import annotations
import logging
from pathlib import Path
from typing import Final, Any, Optional, Union

from rich.logging import RichHandler
from rich import traceback


class Logger:
    """A singleton class to manage logging for the doctree internal modules

    Args:
        logger (logging.Logger): input logger that will be modified and then returned
        output (Path, Optional): Path of log file for file stream handler. If not set, will not log to file.
        modules (dict[str, int], Optional): Optional override of modules / levels. Will be merged into default
            modules.
    """

    _instances: dict[type[Logger], Logger] = {}
    ARROW_HEAD_COUNT: Final = 8
    ARROW_TAIL_COUNT: Final = 14

    def __new__(cls, *_: Any) -> Any:  # noqa https://github.com/PyCQA/pydocstyle/issues/515
        if cls not in cls._instances:
            c = object.__new__(cls)
            cls._instances[cls] = c
            return c
        raise RuntimeError("The logger can only be setup once and this should be done at the top level.")

    def __init__(
        self,
        logger: Any,
        output: Optional[Path] = None,
        modules: Optional[dict[str, int]] = None,
    ) -> None:
        self.modules = {
            # "doctree.file": logging.DEBUG,
        }

        self.logger = logger
        self.modules = {**self.modules, **modules} if modules else self.modules
        self.handlers: list[logging.Handler] = []

        self.file_handler: Optional[logging.Handler]
        if output:
            # Logging to file with millisecond timing
            self.file_handler = logging.FileHandler(output, mode="w")
            file_formatter = logging.Formatter(
                fmt="%(threadName)13s:%(asctime)s.%(msecs)03d %(filename)-40s %(lineno)4s %(levelname)-8s | %(message)s",
                datefmt="%H:%M:%S",
            )
            self.file_handler.setFormatter(file_formatter)
            self.file_handler.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member
            logger.addHandler(self.file_handler)
            self.addLoggingHandler(self.file_handler)
        else:
            self.file_handler = None

        # Use Rich for colorful console logging
        self.stream_handler = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
        stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
        self.stream_handler.setFormatter(stream_formatter)
        self.stream_handler.setLevel(logging.INFO)
        logger.addHandler(self.stream_handler)
        self.addLoggingHandler(self.stream_handler)

        traceback.install()  # Enable exception tracebacks in rich logger

    @classmethod
    def get_instance(cls) -> Logger:
        """Get the singleton instance

        Raises:
            RuntimeError: Has not yet been instantiated

        Returns:
            Logger: singleton instance
        """
        if not (logger := cls._instances.get(Logger, None)):
            raise RuntimeError("Logging must first be setup")
        return logger

    def addLoggingHandler(self, handler: logging.Handler) -> None:
        """Add a handler for all of the internal doctree modules

        Args:
            handler (logging.Handler): handler to add
        """
        self.logger.addHandler(handler)
        self.handlers.append(handler)

        # Enable / disable logging in modules
        for module, level in self.modules.items():
            l = logging.getLogger(module)
            l.setLevel(level)
            l.addHandler(handler)


def setup_logging(
    base: Union[logging.Logger, str], output: Optional[Path] = None, modules: Optional[dict[str, int]] = None
) -> logging.Logger:
    """Configure the doctree modules for logging and get a logger that can be used by the application

    This can only be called once and should be done at the top level of the application.

    Args:
        base (Union[logging.Logger, str]): Name of application (i.e. __name__) or preconfigured logger to use as base
        output (Path, Optional): Path of log file for file stream handler. If not set, will not log to file.
        modules (dict[str, int], Optional): Optional override of modules / levels. Will be merged into default
            modules.

    Raises:
        TypeError: Base logger is not of correct type

    Returns:
        logging.Logger: updated logger that the application can use for logging
    """
    if isinstance(base, str):
        base = logging.getLogger(base)
    elif not isinstance(base, logging.Logger):
        raise TypeError("Base must be of type logging.Logger or str")
    l = Logger(base, output, modules)
    return l.logger

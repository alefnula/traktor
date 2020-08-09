import os
import logging
import contextlib

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def goto(directory, create=False):
    """Context object for changing directory.

    Args:
        directory (str): Directory to go to.
        create (bool): Create directory if it doesn't exists.

    Usage::
        >>> with goto(directory) as ok:
        ...     if not ok:
        ...         print("Error")
        ...     else:
        ...         print("All OK")
    """

    current = os.getcwd()
    directory = os.path.abspath(directory)

    if os.path.isdir(directory) or (
        create and os.makedirs(directory, exist_ok=True)
    ):
        logger.info("goto -> %s", directory)
        os.chdir(directory)
        try:
            yield True
        finally:
            logger.info("goto <- %s", directory)
            os.chdir(current)
    else:
        logger.info(
            "goto(%s) - directory does not exist, or cannot be " "created.",
            directory,
        )
        yield False

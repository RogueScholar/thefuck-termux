from . import read_log
from . import rerun
from . import shell_logger
from ..conf import settings


def get_output(script, expanded):
    """Get output of the script.

    :param script: Console script.
    :type script: str
    :param expanded: Console script with expanded aliases.
    :type expanded: str
    :rtype: str

    """
    if shell_logger.is_available():
        return shell_logger.get_output(script)
    if settings.instant_mode:
        return read_log.get_output(script)
    else:
        return rerun.get_output(script, expanded)

from thefuck.utils import get_all_executables
from thefuck.utils import memoize


@memoize
def _get_executable(script_part):
    for executable in get_all_executables():
        if script_part.startswith(executable):
            return executable


def match(command):
    return not command.script_parts[0] in get_all_executables(
    ) and _get_executable(command.script_parts[0])


def get_new_command(command):
    executable = _get_executable(command.script_parts[0])
    return command.script.replace(executable, u"{} ".format(executable), 1)


priority = 4000

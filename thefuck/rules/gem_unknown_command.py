import re
import subprocess

from thefuck.utils import cache
from thefuck.utils import eager
from thefuck.utils import for_app
from thefuck.utils import replace_command
from thefuck.utils import which


@for_app("gem")
def match(command):
    return ("ERROR:  While executing gem ... (Gem::CommandLineError)" in
            command.output and "Unknown command" in command.output)


def _get_unknown_command(command):
    return re.findall(r"Unknown command (.*)$", command.output)[0]


@eager
def _get_all_commands():
    proc = subprocess.Popen(["gem", "help", "commands"],
                            stdout=subprocess.PIPE)

    for line in proc.stdout.readlines():
        line = line.decode()

        if line.startswith("    "):
            yield line.strip().split(" ")[0]


if which("gem"):
    _get_all_commands = cache(which("gem"))(_get_all_commands)


def get_new_command(command):
    unknown_command = _get_unknown_command(command)
    all_commands = _get_all_commands()
    return replace_command(command, unknown_command, all_commands)

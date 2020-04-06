import re
from subprocess import PIPE
from subprocess import Popen

from thefuck.utils import cache
from thefuck.utils import eager
from thefuck.utils import for_app
from thefuck.utils import replace_argument
from thefuck.utils import replace_command
from thefuck.utils import which

regex = re.compile(r'error Command "(.*)" not found.')


@for_app("yarn")
def match(command):
    return regex.findall(command.output)


npm_commands = {"require": "add"}


@eager
def _get_all_tasks():
    proc = Popen(["yarn", "--help"], stdout=PIPE)
    should_yield = False
    for line in proc.stdout.readlines():
        line = line.decode().strip()

        if "Commands:" in line:
            should_yield = True
            continue

        if should_yield and "- " in line:
            yield line.split(" ")[-1]


if which("yarn"):
    _get_all_tasks = cache(which("yarn"))(_get_all_tasks)


def get_new_command(command):
    misspelled_task = regex.findall(command.output)[0]
    if misspelled_task in npm_commands:
        yarn_command = npm_commands[misspelled_task]
        return replace_argument(command.script, misspelled_task, yarn_command)
    else:
        tasks = _get_all_tasks()
        return replace_command(command, misspelled_task, tasks)

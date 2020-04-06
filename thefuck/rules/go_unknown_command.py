import subprocess
from itertools import dropwhile
from itertools import islice
from itertools import takewhile

from thefuck.utils import cache
from thefuck.utils import for_app
from thefuck.utils import get_closest
from thefuck.utils import replace_argument
from thefuck.utils import which


def get_golang_commands():
    proc = subprocess.Popen("go", stderr=subprocess.PIPE)
    lines = [line.decode("utf-8").strip() for line in proc.stderr.readlines()]
    lines = dropwhile(lambda line: line != "The commands are:", lines)
    lines = islice(lines, 2, None)
    lines = takewhile(lambda line: line, lines)
    return [line.split(" ")[0] for line in lines]


if which("go"):
    get_docker_commands = cache(which("go"))(get_golang_commands)


@for_app("go")
def match(command):
    return "unknown command" in command.output


def get_new_command(command):
    closest_subcommand = get_closest(command.script_parts[1], get_golang_commands())
    return replace_argument(command.script, command.script_parts[1], closest_subcommand)

from thefuck.rules.cd_parent import get_new_command
from thefuck.rules.cd_parent import match
from thefuck.types import Command


def test_match():
    assert match(Command("cd..", "cd..: command not found"))
    assert not match(Command("", ""))


def test_get_new_command():
    assert get_new_command(Command("cd..", "")) == "cd .."

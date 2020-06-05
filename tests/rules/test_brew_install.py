import pytest

from thefuck.rules.brew_install import _get_formulas
from thefuck.rules.brew_install import get_new_command
from thefuck.rules.brew_install import match
from thefuck.types import Command


@pytest.fixture
def brew_no_available_formula():
    return """Error: No available formula for elsticsearch """


@pytest.fixture
def brew_install_no_argument():
    return """This command requires a formula argument"""


@pytest.fixture
def brew_already_installed():
    return """Warning: git-2.3.5 already installed"""


def _is_not_okay_to_test():
    return "elasticsearch" not in _get_formulas()


@pytest.mark.skipif(_is_not_okay_to_test(),
                    reason="No need to run if there's no formula")
def test_match(brew_no_available_formula, brew_already_installed,
               brew_install_no_argument):
    assert match(
        Command("brew install elsticsearch", brew_no_available_formula))
    assert not match(Command("brew install git", brew_already_installed))
    assert not match(Command("brew install", brew_install_no_argument))


@pytest.mark.skipif(_is_not_okay_to_test(),
                    reason="No need to run if there's no formula")
def test_get_new_command(brew_no_available_formula):
    assert (get_new_command(
        Command("brew install elsticsearch",
                brew_no_available_formula)) == "brew install elasticsearch")

    assert (get_new_command(
        Command("brew install aa", brew_no_available_formula)) !=
            "brew install aha")

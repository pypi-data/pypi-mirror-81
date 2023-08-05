import importlib.resources
import os

from click.testing import CliRunner

from pyomodoro.cli import start
import pyomodoro.resources


class TestStart:
    runner = CliRunner()

    def test_float_intervals_are_invalid(self):
        result = self.runner.invoke(start, ['-p', '.5'])
        assert result.exit_code != 0

    def test_command_succeeds(self):
        result = self.runner.invoke(start, ['-d'], input='N')
        assert result.exit_code == 0


def test_icon_ico_exists():
    with importlib.resources.path(pyomodoro.resources, 'pyomodoro.ico') as icon_path:
        assert os.path.isfile(str(icon_path))


def test_icon_png_exists():
    with importlib.resources.path(pyomodoro.resources, 'pyomodoro.png') as icon_path:
        assert os.path.isfile(str(icon_path))

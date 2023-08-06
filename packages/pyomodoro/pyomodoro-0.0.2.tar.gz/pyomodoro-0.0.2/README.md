# Pyomodoro
Pyomodoro is an easy to use CLI for the [Pomodoro Technique](https://francescocirillo.com/pages/pomodoro-technique) written in Python.

[![GitLab pipeline](https://img.shields.io/gitlab/pipeline/tedtramonte/pyomodoro)](https://gitlab.com/tedtramonte/pyomodoro/builds)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyomodoro)](https://pypi.org/project/pyomodoro/)
[![PyPI - License](https://img.shields.io/pypi/l/pyomodoro)](https://choosealicense.com/licenses/mit/)
[![PyPI - Version](https://img.shields.io/pypi/v/pyomodoro)](https://gitlab.com/tedtramonte/pyomodoro/-/releases)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyomodoro)](https://gitlab.com/tedtramonte/pyomodoro)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyomodoro)](https://gitlab.com/tedtramonte/pyomodoro)
[![PyPI - Status](https://img.shields.io/pypi/status/pyomodoro)](https://gitlab.com/tedtramonte/pyomodoro)

## Installation
The best way to install Pyomodoro is to use Pip.

```bash
pip install pyomodoro
```

## Usage
For convenience, both `pom` and `pyomodoro` are available as commands. Pyomodoro operates in your terminal, but if a notification tool is available, Pyomodoro will also send messages that way.

```bash
# Display help text
pom --help
pyomodoro --help

# Begin a session with the standard Francesco Cirillo timing intervals
pom

# Specify a task to focus on before you begin work
pom --ask-task

# Adjust the timing intervals to your liking
pom --pomodoro-length 30 --short-break-length 10 --long-break-length 45
```

## Configuration
There are three ways to adjust the values that Pyomodoro uses:
1. Flags at run time
2. Environment variables
3. YAML config file

|            Flag           |         Env Var        |        YAML        |    Default   |
|:-------------------------:|:----------------------:|:------------------:|:------------:|
| --config-file, -f         | POM_CONFIG_FILE        |                    | ~/.pyomodoro |
| --pomodoro-length, -p     | POM_POMODORO_LENGTH    | pomodoro_length    | 25           |
| --short-break-length, -sb | POM_SHORT_BREAK_LENGTH | short_break_length | 5            |
| --long-break-length, -lb  | POM_LONG_BREAK_LENGTH  | long_break_length  | 20           |
| --ask-task, -t            | POM_ASK_TASK           | ask_task           | False        |
| --dry-run, -d             |                        | dry_run            | False        |

## Contributing
Merge requests are welcome after opening an issue first. Please make sure to update tests as appropriate.

### Development
Since part of Pyomodoro's key feature relies on an accessible notification system, testing that necessitates installing it locally:
```bash
pip install -e .
```

It is also useful to double check how Pyomodoro functions in a containerized environment, as the required tests are run in Docker containers:
```bash
docker run -it -v ${pwd}:/app python bash
cd /app
pip install tox
tox -e py
```

# Pyomodoro
Pyomodoro is an easy to use CLI for the [Pomodoro Technique](https://francescocirillo.com/pages/pomodoro-technique) written in Python.

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
tox -e py
```

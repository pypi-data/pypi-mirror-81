import importlib.resources
from time import sleep

import click
from plyer import notification
from plyer.utils import platform
import pyomodoro.resources


icon = 'pyomodoro.' + ('ico' if platform == 'win' else 'png')


def pomodoro(task, length):
    click.echo(
        f'{task} - Focus on your task for {length} minute{"s" if length != 1 else ""}.'
        ' I\'ll ping you when it\'s time for a break.'
    )
    try:
        with importlib.resources.path(pyomodoro.resources, icon) as icon_path:
            notification.notify(
                title=task,
                message=(f'Focus on your task for {length} minute{"s" if length != 1 else ""}.'
                         ' I\'ll ping you when it\'s time for a break.'),
                app_name='Pyomodoro',
                app_icon=str(icon_path),
            )
        poll_rate = 0.1
        with click.progressbar(range(int(round((length / poll_rate) * 60)))) as bar:
            for _i in bar:
                sleep(poll_rate)
    except UserWarning:
        pass
    except NotImplementedError:
        pass


def take_break(title, message, length):
    click.echo(message)
    try:
        with importlib.resources.path(pyomodoro.resources, icon) as icon_path:
            notification.notify(
                title=title,
                message=message,
                app_name='Pyomodoro',
                app_icon=str(icon_path),
            )
        poll_rate = 0.1
        with click.progressbar(range(int(round((length / poll_rate) * 60)))) as bar:
            for _i in bar:
                sleep(poll_rate)
    except UserWarning:
        pass
    except NotImplementedError:
        pass


def end_break():
    try:
        with importlib.resources.path(pyomodoro.resources, icon) as icon_path:
            notification.notify(
                title='Ready To Continue Focusing?',
                message='Finished with your break and ready to continue focusing?',
                app_name='Pyomodoro',
                app_icon=str(icon_path),
            )
    except UserWarning:
        pass
    except NotImplementedError:
        pass
    return click.confirm(
        'Finished with your break and ready to continue focusing?',
        default=True,
        show_default=True,
        err=True,
    )


@click.command('start', short_help='start a Pomodoro Technique session')
@click.option('--pomodoro-length', '-p', 'pomodoro_length', default=25, show_default=True)
@click.option('--short-break-length', '-sb', 'short_break_length', default=5, show_default=True)
@click.option('--long-break-length', '-lb', 'long_break_length', default=20, show_default=True)
@click.option('--ask-task', '-t', 'ask_task', is_flag=True)
@click.option('--dry-run', '-d', 'dry_run', is_flag=True)
def start(pomodoro_length, short_break_length, long_break_length, ask_task, dry_run):
    """Start a Pomodoro Technique session."""

    if dry_run:
        # Override all lengths with 5 second intervals
        pomodoro_length = 0
        short_break_length = 0
        long_break_length = 0

    if ask_task:
        task = click.prompt('My task is to').title()
    else:
        task = 'Focus'

    focusing = True

    while focusing:
        for pomodoros in range(1, 5):
            click.echo(f'Pomodoro #{pomodoros}')
            pomodoro(task, pomodoro_length)
            if pomodoros < 4:
                take_break(
                    'Take A Short Break',
                    (f'Take a short break for {short_break_length} minute{"s" if short_break_length != 1 else ""}.'
                        ' Stand up and stretch, look out a window, or get some water.'),
                    short_break_length
                )
            else:
                take_break(
                    'Take A Long Break',
                    (f'Take a long break for {long_break_length} minute{"s" if long_break_length != 1 else ""}.'
                        ' You\'ve earned it!'),
                    long_break_length
                )
            focusing = end_break()
            if focusing:
                continue
            else:
                break

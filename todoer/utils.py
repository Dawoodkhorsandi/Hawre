import textwrap
import functools
import shutil

import click
from peewee import ModelSelect, DoesNotExist

from models import TaskModel


def wrap_description_into_multi_line(description: str,
                                     wrap_width: int,
                                     left_padding_for_subsequent_lines: int):
    """
    This utility function divide long description into multi-line string separated by ``\n``
    :param description: Actual description.
    :param wrap_width: Width of result line.
    :param left_padding_for_subsequent_lines: Padding size for second til final line,
                                              padding will not be applied to first line.
    :return: A multiline string to be display in vertical table rows.
    """
    if description is None:
        return '_'

    wrapped_description = textwrap.wrap(description, width=wrap_width)
    multiline_description = ''
    for index, line in enumerate(wrapped_description):
        if index != 0:
            multiline_description += " " * left_padding_for_subsequent_lines
        multiline_description += f'{line}\n'
    return multiline_description


def echo_single_task(task: TaskModel):
    left_padding = 25
    multiline_description = wrap_description_into_multi_line(task.description,
                                                             wrap_width=35,
                                                             left_padding_for_subsequent_lines=left_padding)

    status = click.style("Done", fg='green') if task.is_done else click.style('Not Done', fg='red')

    click.secho(f'{"Task Details":^60}', bg='green', fg='black')
    click.echo(click.style(f'{"Id":<{left_padding}}', fg='green') + f'{task.id}')
    click.echo(click.style(f'{"Name":<{left_padding}}', fg='green') + f'{task.name}')
    click.echo(click.style(f'{"Description":<{left_padding}}', fg='green') + multiline_description)
    click.echo(click.style(f'{"Status":<{left_padding}}', fg='green') + status)
    click.echo(click.style(f'{"Date":<{left_padding}}', fg='green') + f'{task.created_date:%A, %B %d, %Y}')


def echo_task_list(tasks: ModelSelect):
    terminal_width, _ = shutil.get_terminal_size()

    if terminal_width < 75:
        click.secho(f"Warning: Your terminal width is {terminal_width} which is too small,"
                    f" make it wider to display contents correctly.\n\n", fg='yellow')
    id_width = int(terminal_width * 0.04)
    name_width = int(terminal_width * 0.34)
    desc_width = int(terminal_width * 0.44)
    status_width = int(terminal_width * 0.14)
    task_format_string = "{task_id:<{id_width}} {task_name:{name_width}} {desc:{desc_width}} {is_done:{status_width}}"

    click.secho(
        task_format_string.format(
            id_width=id_width,
            task_id="ID",
            name_width=name_width,
            task_name="Name",
            desc="Description",
            desc_width=desc_width,
            is_done="Status",
            status_width=status_width,
        ), bg='green', fg='black')
    for task in tasks:
        click.secho(task_format_string.format(
            task_id=task.id,
            id_width=id_width,
            task_name=task.name,
            name_width=name_width,
            desc=textwrap.shorten(task.description, width=desc_width-3, placeholder="...")
                 if task.description is not None else "-",
            desc_width=desc_width,
            is_done=click.style('Done', fg='green') if task.is_done else click.style("Not Done", fg='red'),
            status_width=status_width,
        ))


def peewee_does_not_exists_error_handler(func):
    """
    A decorator for capture peewee ``DoesNotExist`` and turning it into click appropriate echo output
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except DoesNotExist:
            click.secho(f'Task with id={kwargs.get("task_id")} does not exists in the DB.', fg='red')
    return wrapper

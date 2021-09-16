import click

from models import initialize_db, TaskModel
from utils import (echo_task_list,
                   echo_single_task,
                   peewee_does_not_exists_error_handler,
                   )


@click.group()
def cli():
    """Simple Todo List Program

    Stores added TODO in sqlite DB.
    """


@cli.command('list')
@click.option('-a', '--all', 'include_done_tasks',
              default=False,
              is_flag=True,
              help='Shows all tasks, including done ones.')
@click.option('-d', '--done', 'only_done_tasks',
              default=False,
              is_flag=True,
              help='Only shows done tasks.')
def list_tasks(include_done_tasks: bool,
               only_done_tasks: bool):
    """
    By default returns list of tasks with Not Done status.

    See the options for listing all of them or only done tasks.
    """
    if include_done_tasks and only_done_tasks:
        click.secho("Only one of -d or -a can be used at the same time.", fg='red')
        return
    task_list = TaskModel.list_tasks(include_done_tasks=include_done_tasks,
                                     only_done_tasks=only_done_tasks)
    echo_task_list(task_list)


@cli.command('show')
@click.argument('task_id', type=int)
@peewee_does_not_exists_error_handler
def show_task(task_id: int):
    """
    Show single task using its task_id.
    """
    task = TaskModel.get_task_by_id(task_id=task_id)
    echo_single_task(task)


@cli.command('add')
@click.option('--name', type=str, required=True, help='Name for the task.')
@click.option('--desc', type=str, help='Description for the task.')
def add_task(name: str, desc: str):
    """Adds new task to the DB."""
    TaskModel.create(name=name, description=desc)
    click.secho('Task created successfully.', fg='green')


@cli.command('remove')
@click.argument('task_id', type=int)
@peewee_does_not_exists_error_handler
def remove_task(task_id: int):
    """
    Removes a task from DB by the given task_id.
    """
    TaskModel.delete_task(task_id=task_id)
    click.secho('Task successfully has been deleted.', fg='green')


@cli.command('done')
@click.argument('task_id', type=int)
@peewee_does_not_exists_error_handler
def mark_as_done(task_id: int):
    """
    Marks a task as done in DB for the given task_id.
    """
    TaskModel.mark_task_as_done(task_id=task_id)
    click.secho('Task is now done.', fg='green')


@cli.command('undone')
@click.argument('task_id', type=int)
@peewee_does_not_exists_error_handler
def marks_as_undone(task_id: int):
    """
    Marks a task as undone for the the given task_id.
    """

    TaskModel.mark_task_as_undone(task_id=task_id)
    click.secho('Task is now undone.', fg='green')


def start():
    initialize_db()
    cli()


if __name__ == '__main__':
    start()

from __future__ import annotations

import os
import datetime

from peewee import (Model,
                    SqliteDatabase,
                    CharField,
                    TextField,
                    DateTimeField,
                    BooleanField,
                    ModelSelect,
                    )
DB_NAME = 'tasks.db'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_ABS_PATH = os.path.join(CURRENT_DIR, DB_NAME)
db = SqliteDatabase(DB_ABS_PATH)


class TaskModel(Model):
    name = CharField(max_length=256)
    description = TextField(null=True)
    is_done = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = 'tasks'

    @classmethod
    def list_tasks(cls,
                   include_done_tasks: bool = False,
                   only_done_tasks: bool = False) -> ModelSelect:
        if include_done_tasks:
            return cls.select()
        elif only_done_tasks:
            return cls.select().where(cls.is_done==True)
        return cls.select().where(cls.is_done == False)

    @classmethod
    def get_task_by_id(cls, task_id: int) -> TaskModel:
        return cls.get(cls.id==task_id)

    @classmethod
    def delete_task(cls, task_id: int):
        task = cls.get_task_by_id(task_id)
        task.delete_instance()

    @classmethod
    def mark_task_as_done(cls, task_id: int):
        task = cls.get_task_by_id(task_id)
        task.is_done = True
        task.save()

    @classmethod
    def mark_task_as_undone(cls, task_id: int):
        task = cls.get_task_by_id(task_id)
        task.is_done = False
        task.save()


def initialize_db() -> None:
    db.create_tables([TaskModel,])


def remove_database() -> None:
    try:
        os.remove(DB_ABS_PATH)
    except FileNotFoundError:
        print("DB not found, probably already deleted.")

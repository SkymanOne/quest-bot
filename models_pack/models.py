#! /usr/bin/env python
# -*- coding: utf8 -*-
from peewee import *
from datetime import datetime
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')
path_to_db = parser['DATABASE']['path']
if path_to_db is not None:
    db = SqliteDatabase(path_to_db)
else:
    db = SqliteDatabase('db_week.db')


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    game_name = CharField()
    game_description = TextField()
    game_timer = IntegerField()
    max_score = IntegerField()


class Task(BaseModel):
    task_text = TextField()
    task_answer = TextField()
    task_game = ManyToManyField(Game, backref='tasks')
    task_level = IntegerField()
    task_bonus = IntegerField()
    task_photo = BlobField(null=True, default=None)
    task_file = BlobField(null=True, default=None)


class User(BaseModel):
    user_name = CharField()
    user_telegram_id = IntegerField()
    user_all_score = IntegerField(default=0)
    user_current_game = ForeignKeyField(Game)
    user_tries = IntegerField(default=3)
    user_game_level = IntegerField(default=0)
    user_game_start = DateTimeField(null=True)
    user_game_end = DateTimeField(null=True)


class UserFinishedGame(BaseModel):
    user_telegram_id = IntegerField()
    user_game = ForeignKeyField(Game)


class Winner(BaseModel):
    winner_user = ForeignKeyField(User)
    winner_game = ForeignKeyField(Game)
    best_time = DateTimeField()

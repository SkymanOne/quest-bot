from peewee import *
from playhouse.migrate import *
from playhouse.fields import *
from datetime import datetime

import models_pack

db = SqliteDatabase('vneurokabot.db')
migrator = SqliteMigrator(db)


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

    @classmethod
    def get_levels_of_game(cls, game_name):
        level = Game.get(Game.game_name == game_name).tasks.count()
        return level


class User(BaseModel):
    user_name = CharField()
    user_telegram_id = IntegerField()
    user_all_score = IntegerField(default=0)
    user_current_game = ForeignKeyField(Game)
    user_game_level = IntegerField(default=0)
    user_game_start = DateTimeField(null=True)
    user_game_end = DateTimeField(null=True)


class Winner(BaseModel):
    winner_user = ForeignKeyField(User)
    winner_game = ForeignKeyField(Game)
    best_time = DateTimeField()

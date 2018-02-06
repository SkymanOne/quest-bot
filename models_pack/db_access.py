from peewee import *
from models_pack.models import *
from telebot import types
from models_pack.constants import *


def create_user(user: types.User, time):
    new_user = User(user_name=user.first_name, user_surname=user.last_name, user_id=user.id,
                    user_start_game=time)
    new_user.save()


def get_user(id_user):
    try:
        user = User.get(User.user_id == id_user)
    except DoesNotExist:
        return None
    else:
        return user


def get_level(id_user):
    user = get_user(id_user)
    if user is not None:
        return user.user_level
    else:
        return 0


def set_level(id_user, number_level):
    user = get_user(id_user)
    if user is not None:
        user.user_level = number_level
        user.save()
    else:
        return None

#! /usr/bin/env python
# -*- coding: utf8 -*-
from models_pack.models import *
import my_loging
import mypy
import os


def create_game(name, description, timer, score):
    try:
        Game.create(game_name=name, game_description=description,
                    game_timer=timer, max_score=score)
    except Exception:
        my_loging.error('Ошибка создания игры: ' + name)
    else:
        my_loging.info('Создана игра: ' + name
                       + ' - описание: ' + description
                       + ' - таймер: ' + str(timer) + ' макс. счет: ' + str(score))


def search_game(name: str):
    """

    :param name: string name of your game
    :return: None, if game was not found
    :return: object of Game
    """
    try:
        game = Game.get(Game.game_name == name)
        my_loging.warning('Игра ' + name + ' найдена')
    except DoesNotExist:
        my_loging.warning('Игра ' + name + ' не найдена')
        return None
    else:
        return game


def delete_game(name: str):
    game = search_game(name)
    if game is not None:
        game.delete()
        my_loging.info('Игра - ' + name + ' - успешно удалена')
        return True
    else:
        my_loging.error('Ошибка удаление игры')
        return False


def create_task(text: str, answer: str, game_name: str,
                bonus: int, photo=None, file=None):
    global new_task
    try:
        game = search_game(game_name)
        if game is not None:
            level = get_tasks_of_game(game_name).count() + 1
            new_task = Task.create(task_text=text, task_answer=answer,
                                   task_level=level, task_bonus=bonus,
                                   task_photo=photo, task_file=file)
            new_task.task_game.add([game])
            game.max_score += bonus
            game.save()
            new_task.save()
            my_loging.info('Создано задание в игре - ' + game_name)
        else:
            my_loging.error('Ошибка создания задания')
            return None
    except Exception:
        my_loging.error('Ошибка создания создания')
        return None
    else:
        return new_task


def get_task(game_name: str, level: int):
    game = search_game(game_name)
    global task
    if game is None:
        my_loging.error('Ошибка поиска задания')
        return None
    else:
        try:
            tasks = get_tasks_of_game(game_name)
            for t in tasks:
                if t.task_level == level:
                    task = t
            print(task.task_text)
        except Exception:
            my_loging.error('Ошибка поиска задания')
            return None
        else:
            return task


def get_tasks_of_game(game_name: str):
    try:
        levels = Game.get(Game.game_name == game_name).tasks
    except Game.DoesNotExist:
        my_loging.error('Ошибка поиска задания')
        return False
    return levels


def delete_task(game_name: str, level: int):
    task = get_task(game_name, level)
    if task is None:
        my_loging.error('Ошибка удаление задания под номером: ' + str(level))
        return False
    else:
        task.delete_instance()
        my_loging.error('Удаление задания под номером: ' + str(level))

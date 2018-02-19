#! /usr/bin/env python
# -*- coding: utf8 -*-
from models_pack.models import *
import my_loging
from datetime import datetime
import mypy
import os


def create_game(name, description, timer, score):
    my_loging.info('Вызов метода создания игры')
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
    my_loging.info('Вызов метода поиск игры')
    """

    :param name: string name of your game
    :return: None, if game was not found
    :return: object of Game
    """
    try:
        game = Game.get(Game.game_name == name)
        my_loging.warning('Игра ' + name + ' найдена')
    except DoesNotExist:
        my_loging.error('Игра ' + name + ' не найдена')
        return None
    else:
        return game


def delete_game(name: str):
    my_loging.info('Вызов метода удаления игры')
    game = search_game(name)
    if game is not None:
        tasks = get_tasks_of_game(name)
        for t in tasks:
            t.delete_instance()
        game.delete_instance()
        my_loging.info('Игра - ' + name + ' - успешно удалена')
        return True
    else:
        my_loging.error('Ошибка удаление игры')
        return False


def create_task(text: str, answer: str, game_name: str,
                bonus: int, photo=None, file=None):
    my_loging.info('Вызов метода создания задания')
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
    my_loging.info('Вызов метода получения задания')
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
    my_loging.info('Вызов метода получения списка заданий игры')
    try:
        levels = Game.get(Game.game_name == game_name).tasks
    except Game.DoesNotExist:
        my_loging.error('Ошибка поиска заданий')
        return False
    return levels


def delete_task(game_name: str, level: int):
    my_loging.info('Вызов метода удаления задания')
    task = get_task(game_name, level)
    if task is None:
        my_loging.error('Ошибка удаление задания под номером: ' + str(level))
        return False
    else:
        task.delete_instance()
        tasks = get_tasks_of_game(game_name)
        for t in tasks:
            if t.task_level > level:
                t.task_level -= 1
                t.save()
        my_loging.error('Удаление задания под номером: ' + str(level))


def create_user(name: str, telegram_id: int, game_name: str, game_start=None):
    my_loging.info('Вызов метода создания пользователя')
    game = search_game(game_name)
    if game is not None:
        try:
            my_loging.info('Регистрация нового пользователя')
            User.create(user_name=name, user_telegram_id=telegram_id,
                        user_current_game=game, user_game_start=game_start)
            my_loging.info('Пользователь ' + name + ' успешно зарегистрирован')
            return True
        except Exception:
            my_loging.error('Ошибка регистрации нового пользователя')
    else:
        my_loging.error('Ошибка поиска игры')
        return False


def get_user(telegram_id: int):
    my_loging.info('Вызов метода для получение пользователя')
    try:
        my_loging.info('Поиск пользователя с id ' + str(telegram_id) + ' в базе данных')
        user = User.get(User.user_telegram_id == telegram_id)
    except DoesNotExist:
        my_loging.error('Пользователь не найден')
        return None
    else:
        return user


def delete_user(telegram_id: int):
    my_loging.info('Вызов метода для удаления пользователя')
    user = get_user(telegram_id)
    if user is not None:
        my_loging.warning('удаление пользваотеля с id ' + str(telegram_id))
        user.delete_instance()
        my_loging.info('пользователь удален')
        return True
    else:
        my_loging.error('Ошибка удаления пользователя')
        return False


def create_winner(user_telegram_id: int, game_name: str, best_time: datetime):
    my_loging.info('Вызов метода для добавления победителя')
    winner = get_user(user_telegram_id)
    game = search_game(game_name)
    if winner is not None and game is not None:
        Winner.create(winner_user=winner, winner_game=game, best_time=best_time)
        my_loging.info('Победитель в игре ' + game_name + ' с id ' + str(user_telegram_id) +
                       ' pуспешно зарегистрирован')
        return True
    else:
        my_loging.error('Ошибка добавления победителя')
        return False

# TODO: метод для добавления победителя
# TODO: метод для удаление победителя

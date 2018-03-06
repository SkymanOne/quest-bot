#! /usr/bin/env python
# -*- coding: utf8 -*-
from models_pack.models import *
from models_pack import my_loging
from datetime import datetime


def init_db():
    my_loging.info('Инициализация базы данных по пути: {path}'
                   .format(path=path_to_db))
    try:
        db.create_tables([
            Game,
            Task,
            User,
            Winner,
            UserFinishedGame,
            Task.task_game.get_through_model()
        ], safe=True)
        my_loging.info('Инициализация базы данных прошла успешно')
        return True
    except:
        my_loging.error('Ошибка инициализация базы данных')
        return False


def create_game(game_name: str, description: str, timer: str, score: int):
    """
    function of creating game

    :param game_name: name of your game
    :param description: description of game
    :param timer: time, when game will work
    :param score: start score
    :return: object of created game or None, if there was errors
    """
    my_loging.info('Вызов метода создания игры')
    try:
        Game.create(game_name=game_name, game_description=description,
                    game_timer=timer, max_score=score)
    except Exception:
        my_loging.error('Ошибка создания игры: ' + game_name)
    else:
        my_loging.info('Создана игра: ' + game_name
                       + ' - описание: ' + description
                       + ' - таймер: ' + str(timer) + ' макс. счет: ' + str(score))


def search_game(game_name: str):
    """
        searching game in database, who was connect

        :param game_name: string name of your game
        :return: None, if game was not found
        :return: object of Game
        """
    my_loging.info('Вызов метода поиск игры')
    try:
        game = Game.get(Game.game_name == game_name)
        my_loging.info('Игра {name} найдена в базе данных'.format(name=game_name))
    except DoesNotExist:
        my_loging.error('Игра {name} не найдена в базе данных'.format(name=game_name))
        return None
    else:
        return game


def get_all_games():
    """
    get list of all games in app.

    :return: list of all games or None
    """
    my_loging.info('Вызов метода для получения списка всех игр.')
    try:
        games = Game.select()
        my_loging.info('Получение игр из базы данных')
        return games
    except DoesNotExist:
        my_loging.error('Ошибка получения игр')
        return None


def delete_game(game_name: str):
    my_loging.info('Вызов метода удаления игры')
    game = search_game(game_name)
    if game is not None:
        tasks = get_tasks_of_game(game_name)
        for t in tasks:
            t.task_game.remove(game)
            t.delete_instance()
        game.delete_instance()
        my_loging.info('Игра - ' + game_name + ' - успешно удалена')
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
            new_task = Task.create(task_text=text, task_answer=answer.lower(),
                                   task_level=level, task_bonus=bonus,
                                   task_photo=photo, task_file=file)
            game.tasks.add(new_task)
            game.max_score += bonus
            game.save()
            new_task.save()
            my_loging.info('Создано задание в игре - ' + game_name)
        else:
            my_loging.error('Ошибка создания задания')
            return None
    except DoesNotExist:
        my_loging.error('Ошибка создания задания')
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
    deleting_task = get_task(game_name, level)
    game = search_game(game_name)
    if deleting_task is None and game is not None:
        my_loging.error('Ошибка удаление задания под номером: ' + str(level))
        return False
    else:
        game.max_score -= deleting_task.task_bonus
        game.save()
        deleting_task.task_game.remove(search_game(game_name))
        deleting_task.delete_instance()
        tasks = get_tasks_of_game(game_name)
        for t in tasks:
            if t.task_level > level:
                t.task_level -= 1
                t.save()
        my_loging.warning('Удалено задания под номером: ' + str(level))


def create_user(user_name: str, telegram_id: int, game_name: str, game_start=None):
    my_loging.info('Вызов метода создания пользователя')
    game = search_game(game_name)
    if game is not None:
        try:
            my_loging.info('Регистрация нового пользователя')
            User.create(user_name=user_name, user_telegram_id=telegram_id,
                        user_current_game=game, user_game_start=game_start)
            my_loging.info('Пользователь ' + user_name + ' успешно зарегистрирован')
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


def get_all_users():
    """
    Get all users in app from db.

    :return: list of all users or None
    """
    my_loging.info('Вызов метод для получения списка всех пользователей')
    try:
        my_loging.info('получение списка всех пользователей')
        users = User.select()
        return users
    except DoesNotExist:
        my_loging.error('Ошибка получения списка пользователей')


def get_all_users_by_score():
    """
    Get all users in app from db.

    :return: list of all users or None
    """
    my_loging.info('Вызов метод для получения списка всех пользователей по очкам')
    try:
        my_loging.info('получение списка всех пользователей...')
        users = User.select().order_by(-User.user_all_score)
        return users
    except DoesNotExist:
        my_loging.error('Ошибка получения списка пользователей')


def get_users_of_game_by_score(game_name: str):
    """
    func., who select users from db

    :param game_name:
    :return: list of users in game or None, if game wasn't found
    """
    my_loging.info('Вызов метода для получения пользователей в игре')
    game = search_game(game_name)
    if game is not None:
        my_loging.info('Поиск игроков...')
        users = User.select(User.user_current_game == game).order_by(User.user_all_score)
        my_loging.info('Игроки найдены в игре {game}'.format(game=game_name))
        return users
    else:
        my_loging.error('Ошибка поиска игроков в базе данных (игра не найдена)')
        return None


def up_user_score(telegram_id: int, changing_score: int):
    my_loging.info('Вызов метода для изменения очков пользователя')
    user = get_user(telegram_id)
    if user is not None:
        user.user_all_score += changing_score
        user.save()
        return True
    else:
        my_loging.error('Ошибка пополнения очков у пользователя (пользователь не найден)')
        return None


def end_user_playing(telegram_id, end_of_game: datetime):
    my_loging.info('Вызов метода для изменения окончания игры пользователя')
    user = get_user(telegram_id)
    if user is not None:
        user.user_game_end = end_of_game
        user.save()
        return True
    else:
        my_loging.error('Ошибка изменения окончания игры у пользователя (пользователь не найден)')
        return None


def change_user_game(telegram_id: int, new_game_name: str):
    my_loging.info('Вызов метода для изменения игры')
    user = get_user(telegram_id)
    game = search_game(new_game_name)
    if user is not None and game is not None:
        my_loging.info('Обновление текущей игры пользователя - {user}'.format(user=user.user_name))
        user.user_current_game = game
        user.save()
        my_loging.info('Игра успешно обновлена')
        return True
    else:
        my_loging.error('Ошибка обновления игры пользователя')
        return False


def down_user_tries(telegram_id: int, count):
    my_loging.info('Вызов метода для изменения попыток пользователя')
    user = get_user(telegram_id)
    if user is not None:
        user.user_tries -= count
        user.save()
        return True
    else:
        my_loging.error('Ошибка изменения попыток у пользователя (пользователь не найден)')
        return None


def restore_user_tries(telegram_id: int):
    my_loging.info('Вызов метода для восстановления попыток пользователя')
    user = get_user(telegram_id)
    if user is not None:
        user.user_tries = 3
        user.save()
        return True
    else:
        my_loging.error('Ошибка воссталновления попыток у пользователя (пользователь не найден)')
        return None


def change_user_level(telegram_id: int, set_level: int):
    my_loging.info('Вызов метода для изменения текущего уровня игры у пользователя с id: {tel_id}'
                   .format(tel_id=telegram_id))
    user = get_user(telegram_id)
    if user is not None:
        user.user_game_level = set_level
        user.save()
        my_loging.info('Успешное обновление уровня пользователя')
        return True
    else:
        my_loging.error('Ошибка изменения текущего уровня игры у пользователя с id: {tel_id}'
                        .format(tel_id=telegram_id))
        return False


def change_game_of_user(telegram_id: int, set_game_name: str):
    my_loging.info('Вызов метода для изменения текущей игры у пользователя с id: {tel_id}'
                   .format(tel_id=telegram_id))
    user = get_user(telegram_id)
    game = search_game(set_game_name)
    if user is not None and game is not None:
        user.user_current_game = game
        user.save()
        my_loging.info('Успешное обновление игры пользователя')
        return True
    else:
        my_loging.error('Ошибка изменения текущей игры у пользователя с id: {tel_id}'
                        .format(tel_id=telegram_id))
        return False


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


def create_user_finished_game(telegram_id: int, game: Game):
    my_loging.info('Вызов метода для записи окончания игры пользователя')
    user = get_user(telegram_id)
    if game is not None and user is not None:
        UserFinishedGame.create(user_telegram_id=telegram_id, user_game=game)
        my_loging.info('Пользователь с id {id} успешно закончил игру'.format(id=telegram_id))
        return True
    else:
        my_loging.error('Ошибка записи окончания пользователя')
        return False


def is_user_finished_game(telegram_id: int, game: Game):
    try:
        my_loging.info('Получение окончившего игру пользователя - {id}'.format(id=telegram_id))
        user = UserFinishedGame.get(UserFinishedGame.user_telegram_id == telegram_id,
                                    UserFinishedGame.user_game == game)
    except DoesNotExist:
        my_loging.info('Ошибка получения окончившего игру пользователя')
        return False
    else:
        my_loging.info('Успешное получение пользователя с id - {id}'.format(id=telegram_id))
        return True


def create_winner(user_telegram_id: int, game_name: str, best_time: datetime):
    my_loging.info('Вызов метода для добавления победителя')
    winner = get_user(user_telegram_id)
    game = search_game(game_name)
    if winner is not None and game is not None:
        Winner.create(winner_user=winner, winner_game=game, best_time=best_time)
        my_loging.info('Победитель в игре ' + game_name + ' с id ' + str(user_telegram_id) +
                       ' успешно зарегистрирован')
        return True
    else:
        my_loging.error('Ошибка добавления победителя')
        return False


def get_winner(user_telegram_id: int, game_name: str):
    global name
    my_loging.info('Вызов метода для поиска победителя')
    user = get_user(user_telegram_id)
    game = search_game(game_name)
    if user is not None and game is not None:
        try:
            name = user.user_name
            my_loging.info('Поиск победителя в базе данных')
            winner = Winner.get(Winner.winner_user == user and Winner.winner_game == game)
        except DoesNotExist:
            my_loging.error('Победитель {name} не найден в базе даных'.format(name=name))
            return None
        else:
            my_loging.info('Победитель {name} найден в базе даных'.format(name=name))
            return winner
    else:
        my_loging.error('Ошибка поиска победителя {name} в базе данных'.format(name=name))
        return None


def delete_winner(user_telegram_id: int, game_name: str):
    global name
    my_loging.info('Вызов метода для удаления победителя')
    winner = get_winner(user_telegram_id, game_name)
    if winner is not None:
        name = winner.winner_user.user_name
        my_loging.info('Удаление победителя {name}'.format(name=name))
        winner.delete_instance()
        my_loging.warning('Победитель {name} успешно удален'.format(name=name))
        return True
    else:
        my_loging.error('Ошибка удаления победителя с id - {id}'.format(id=user_telegram_id))
        return False

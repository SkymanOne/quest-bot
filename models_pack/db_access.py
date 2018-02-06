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
                       + '\nописание: ' + description
                       + '\nтаймер: ' + str(timer) + ' макс. счет: ' + str(score))


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
        my_loging.info('Игра ' + name + ' успешно удалена')
    else:
        my_loging.error('Ошибка удаление игры')


def create_task(text: str, answer: str, game_name: str, level: int,
                bonus: int, photo, file):
    game = search_game(game_name)
    if game is None:
        my_loging.error('Ошибка создания задания')
        return None
    else:
        try:
            new_task = Task.create(task_text=text, task_answer=answer, task_game=game,
                                   task_level=level, task_bonus=bonus,
                                   task_photo=photo, task_file=file)
        except Exception:
            my_loging.error('Ошибка создания создания')
            return None
        else:
            return new_task


def get_task(game_name: str, level: int):
    game = search_game(game_name)
    if game is None:
        my_loging.error('Ошибка поиска задания')
        return None
    else:
        try:
            task = Task.get(Task.task_game == game and Task.task_level == level)
        except Exception:
            my_loging.error('Ошибка поиска задания')
            return None
        else:
            return task


def get_list_of_game_tasks(game_name: str):
    game = search_game(game_name)
    if game is None:
        my_loging.error('Ошибка получения списка заданий')
        return None
    else:
        list_task = Task.select().where(Task.task_game == game)
    return list_task


def delete_task(game_name: str, level: int):
    task = get_task(game_name, level)
    if task is None:
        my_loging.error('Ошибка удаление задания под номером: ' + str(level))

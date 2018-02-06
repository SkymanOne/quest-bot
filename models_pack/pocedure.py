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
        my_loging.error('Ощибка создания задания')
    # TODO: дописать созздание задания





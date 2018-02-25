#! /usr/bin/env python
# -*- coding: utf8 -*-
import click
from models_pack import db_access, my_loging
import os


def readfile(path=None):
    if os.path.exists(path):
        global fin
        try:
            fin = open(path, 'rb')
            img = fin.read()
            return img
        except IOError:
            return None
        finally:
            if fin:
                fin.close()
    else:
        return None


@click.group()
def cli():
    pass


@cli.command()
def init():
    result = db_access.init_db()
    if result is True:
        click.echo('Инициализация базы данных прошла успешно')
    elif result is False:
        click.echo('Ошибка инициализации базы данных')


@cli.command()
@click.option('--name', '-n', type=str, help='Name of your game', prompt=True)
@click.option('--description', '-d', type=str, help='Description of your game',
              prompt=True)
@click.option('--timer', '-t', type=int, help='Time of your game',
              prompt=True)
@click.option('--score', '-s', type=int, help='Max score of your game',
              prompt=True)
def reg_game(name, description, timer, score):
    """Register your game."""
    my_loging.info('Ввод данных с клавиатуры для создания игры')
    db_access.create_game(name, description, timer, score)
    click.echo('Игра ' + name + ' успешно зарегистрирована')


@cli.command()
@click.option('--name', '-n', type=str, help='Name of deleting game', prompt=True)
@click.confirmation_option(prompt='are you sure to delete this game?')
def del_game(name):
    """Delete your game."""
    my_loging.info('Ввод данных игры для удаления')
    res = db_access.delete_game(name)
    if res:
        click.echo('Игра ' + name + ' успешно удалена')
    else:
        click.echo('Игра ' + name + ' не найдена')


@cli.command()
@click.option('--game_name', '-gm', type=str, help='Name of game', prompt=True)
@click.option('--text', '-t', type=str, help='Text of task', prompt=True)
@click.option('--answer', '-a', type=str, help='Answer of task', prompt=True)
@click.option('--bonus', '-b', type=int, help='Bonus of task', prompt=True)
def reg_task(game_name, text, answer, bonus):
    """Add task for game."""
    my_loging.info('Ввод данных задания для регистрации')
    path_for_photo = click.prompt('Insert path to photo', type=str, default=None)
    photo = readfile(path_for_photo)
    path_for_file = click.prompt('Insert path to file', type=str, default=None)
    file = readfile(path_for_file)
    result = db_access.create_task(text, answer, game_name, bonus, photo, file)
    if result is not None:
        click.echo('Задание  для игры ' + game_name +
                   ' успешно добавлено')
    else:
        click.echo('Ошибка добавления задания')


@cli.command()
@click.option('--name', '-n', type=str, help='Name of your game', prompt=True)
def get_tasks(name):
    """Get tasks of your game."""
    my_loging.info('Ввод данных вывода заданий')
    tasks = db_access.get_tasks_of_game(name)
    if tasks is not False:
        for t in tasks:
            m = t.task_text
            l = t.task_level
            a = t.task_answer
            b = t.task_bonus
            click.echo('\n --------------- \n' +
                       'Text - ' + m + '\nLevel - ' + str(l) +
                       '\nAnswer - ' + a +
                       '\nBonus - ' + str(b))
    else:
        my_loging.error('Ошибка вывода заданий игры')
        click.echo('Ошибка вывода заданий задания')


@cli.command()
@click.option('--name', '-n', type=str, help='Name of your game', prompt=True)
@click.option('--level', '-l', type=int, help='Delete level of your game', prompt=True)
@click.confirmation_option(prompt='are you sure to delete this game?')
def del_task(name, level):
    """Delete task of your game."""
    my_loging.info('Ввод данных для удаления задания')
    if db_access.delete_task(name, level) is False:
        click.echo('Ошибка удаления задания')
    else:
        click.echo('Уровень ' + str(level) + ' успешно удален')


if __name__ == '__main__':
    cli()

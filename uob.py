import click
import my_loging
from models_pack import db_access


@click.group()
def cli():
    pass


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
    my_loging.info('Ввод данных задания для регистрации')
    result = db_access.create_task(text, answer, game_name, bonus)
    if result is not None:
        click.echo('Задание  для игры ' + game_name +
                   ' успешно добавлено')
    else:
        click.echo('Ошибка добавления задания')


if __name__ == '__main__':
    cli()

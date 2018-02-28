import telebot
from telebot import types
from models_pack import db_access, my_loging
from token_const import token

bot = telebot.TeleBot(token)


def parse_user(message: types.Message):
    info = '{name} {surname} ({user_id})'.\
        format(name=message.from_user.first_name,
               surname=message.from_user.last_name,
               user_id=message.from_user.id)
    return info


def get_main_markup():
    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('Начать игру⛳️', 'Лидеры по играм⚜️')
    main_markup.row('Справка🌚', 'Рейтинг игр')
    return main_markup


def get_games_markup():
    games_markup = types.ReplyKeyboardMarkup()
    list_of_games = db_access.get_all_games()
    for game in list_of_games:
        games_markup.row(game.game_name)
    games_markup.row('Главное меню✅')
    return games_markup


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Главное меню✅')
def main_start(message: types.Message):
    my_loging.info('{user} -- начата работа с ботом, нажата кнопка /start или Гавное меню'
                   .format(user=parse_user(message)))
    bot.send_message(message.from_user.id, 'Приветствую тебя, ' + message.from_user.first_name
                     + ', что желаешь?', reply_markup=get_main_markup())


@bot.message_handler(func=lambda message: message.text == 'Начать игру⛳️')
@bot.message_handler(func=lambda message: message.text == 'Рейтинг игр')
def show_games(message: types.Message):
    if message.text == 'Начать игру⛳️':
        list_of_games = db_access.get_all_games()
        for game in list_of_games:
            text = '{gname}\n\n{gtext}'.format(gname=game.game_name,
                                               gtext=game.game_description)
            bot.send_message(message.from_user.id, text)
        msg = bot.send_message(message.from_user.id, 'Выбери игру для начала',
                               reply_markup=get_games_markup())
        bot.register_next_step_handler(msg, start_game)
    elif message.text == 'Рейтинг игр':
        msg = bot.send_message(message.from_user.id, 'Выбери игру',
                               reply_markup=get_games_markup())
        bot.register_next_step_handler(msg, rating_of_games)


def start_game(message: types.Message):
    game = db_access.search_game(message.text)
    if game is None:
        bot.send_message(message.from_user.id, 'Игру не выбрали',
                         reply_markup=get_main_markup())
    else:
        pass


def rating_of_games(message: types.Message):
    game = db_access.search_game(message.text)
    if game is None:
        bot.send_message(message.from_user.id, 'Игру не выбрали',
                         reply_markup=get_main_markup())
    else:
        pass


bot.polling(True)
# TODO: переписать логику: сначала выбор действия(начало игры, рейтинг и тп), а потом выбор игры
# TODO: прописать логику перехода по уровням
# TODO: сделать всё до четверга

import telebot
from telebot import types
from models_pack import db_access, my_loging
from token_const import token

bot = telebot.TeleBot(token)

main_markup = types.ReplyKeyboardMarkup()
main_markup.row('Доступные игры📲', 'Лидеры по играм⚜️')
main_markup.row('Справка🌚')


games_markup = types.ReplyKeyboardMarkup()
list_of_games = db_access.get_all_games()
for game in list_of_games:
    games_markup.row(game.game_name)
games_markup.row('Главное меню✅')


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Главное меню✅')
def main_start(message: types.Message):
    my_loging.info('{user} -- начата работа с ботом, нажата кнопка /start или Гавное меню'
                   .format(user=message.from_user.first_name))
    bot.send_message(message.from_user.id, 'Приветствую тебя, ' + message.from_user.first_name
                     + ', что желаешь?', reply_markup=main_markup)


@bot.message_handler(func=lambda message: message.text == 'Доступные игры📲')
def aviable_games(message: types.Message):
    msg = bot.send_message(message.from_user.id, 'Вот тебе список доступных игр',
                           reply_markup=games_markup)
    bot.register_next_step_handler(msg, game_info)


def game_info(message: types.Message):
    if message.text == 'Главное меню✅':
        bot.send_message(message.from_user.id, 'Главное меню',
                         reply_markup=main_markup)
    else:
        game = db_access.search_game(message.text)
        if game is not None:
            markup = types.ReplyKeyboardMarkup()
            markup.row('Начать игру⛳️', 'Рейтинг📊')
            markup.row('Победители', 'Доступные игры📲')
            msg = bot.send_message(message.from_user.id, game.game_description,
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, options_of_game)
        else:
            bot.send_message(message.from_user.id, 'Ошибка поиска игры')


def options_of_game(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    current_game = user.user_current_game
    if message.text == 'Начать игру⛳️':
        user = db_access.get_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Ткест')
        if user is None:
            db_access.create_user(message.from_user.first_name, message.from_user.id, current_game.game_name)
            bot.send_message(message.from_user.id, 'Вы зареганы')
        else:
            db_access.change_user_game(message.from_user.id, message.text)
            bot.send_message(message.from_user.id, 'Игра изменена')
    elif message.text == 'Рейтинг📊':
        pass
    elif message.text == 'Победители':
        pass
    else:
        bot.send_message(message.from_user.id, 'Доступные игры', reply_markup=games_markup)


bot.polling(True)

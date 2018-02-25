import telebot
from telebot import types
from models_pack import db_access, my_loging
from token_const import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Главное меню✅')
def main_start(message: types.Message):
    my_loging.info('{user} -- начата работа с ботом, нажата кнопка /start или Гавное меню'.format(user=message.from_user))
    markup = types.ReplyKeyboardMarkup()
    markup.row('Доступные игры📲', 'Лидеры по играм⚜️')
    markup.row('Справка🌚')
    bot.send_message(message.from_user.id, 'Приветствую тебя, ' + message.from_user.first_name
                     + ', что желаешь?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Доступные игры📲')
def aviable_games(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    list_of_games = db_access.get_all_games()
    for game in list_of_games:
        markup.row(game.game_name)
    markup.row('Главное меню✅')
    msg = bot.send_message(message.from_user.id, 'Вот тебе список доступных игр',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, game_info)


def game_info(message: types.Message):
    game = db_access.search_game(message.text)
    if game is not None:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Начать игру⛳️', 'Рейтинг📊')
        markup.row('Победители', 'Доступные игры📲')
        msg = bot.send_message(message.from_user.id, game.game_description,
                               reply_markup=markup)
        if msg.text == 'Начать игру⛳️':
            if db_access.get_user(message.from_user.id) is None:
                db_access.create_user(message.from_user.first_name, message.from_user.id, game.game_name)
            bot.register_next_step_handler(msg, start_game)
        elif msg.text == 'Рейтинг📊':
            pass
        elif msg.text == 'Победители':
            pass

    else:
        bot.send_message(message.from_user.id, 'Ошибка поиска игры')


def start_game(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    game = user.user_current_game
    bot.send_message(message.from_user.id, 'Вы начали игру: {game}'.format(game=game.game_name))


bot.polling(True)

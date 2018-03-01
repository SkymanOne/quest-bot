import telebot
from telebot import types
from models_pack import db_access, my_loging
from token_const import token
from datetime import datetime

bot = telebot.TeleBot(token)


def parse_user(message: types.Message):
    info = '{name} {surname} ({user_id})'.\
        format(name=message.from_user.first_name,
               surname=message.from_user.last_name,
               user_id=message.from_user.id)
    return info


def get_main_markup():
    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('Start game⛳️', 'Leaders of game⚜️')
    main_markup.row('About🌚', 'About developer')
    return main_markup


def get_task_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Get task🔄', 'End the game😒')
    return markup


@bot.message_handler(commands=['start'] and db_access.get_user())
def main_start(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    if user is None:
        game = db_access.search_game('English videos')
        if game is not None:
            string = 'The game⛳️ in which you must listen to what the students😎 are talking about and guess what ' \
                     'word is being spoken about.\nSo, you have 3 attempts to guess what word is at stake, ' \
                     'for the right answer you get points✅.\nIf you did not manage to guess the word, ' \
                     'you get 0 points for it😒.\n\nGood luck🤪! '
            msg = bot.send_message(message.from_user.id, 'English videos\n\n' + string,
                                   reply_markup=get_main_markup(), parse_mode='HTML')
            bot.register_next_step_handler(msg, options_game)
    else:
        bot.send_message(message.from_user.id, 'Are you in Game! 😎')
        bot.send_message(message.from_user.id, 'Click on the button to get the task 📝',
                         reply_markup=get_task_markup())


def options_game(message: types.Message):
    if message.text == 'Start game⛳️':
        result = db_access.create_user(message.from_user.first_name, message.from_user.id, 'English videos',
                                       game_start=datetime.now())
        if result:
            bot.send_message(message.from_user.id, 'Are you in Game! 😎')
            bot.send_message(message.from_user.id, 'Click on the button to get the task 📝',
                             reply_markup=get_task_markup())


bot.polling(True)

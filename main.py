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
    main_markup.row('Начать игру⛳️', 'Лидеры по игре⚜️')
    main_markup.row('Справка🌚', 'О разработчике')
    return main_markup


bot.polling(True)
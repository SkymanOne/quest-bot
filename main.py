import telebot
from telebot import types
import logging
from models_pack import db_access
from datetime import datetime
import os
from flask import Flask, request

token = os.environ.get('TOKEN')

bot = telebot.TeleBot(token)

about_me = 'German Nikolishin\n\nPython and .NET developer👨‍💻\nTelegram👉 @german_nikolishin\nGitHub👉 ' \
           'https://github.com/SkymanOne\nVK👉 https://vk.com/german_it\nInst👉 ' \
           'https://www.instagram.com/german.nikolishin/\nTelegram Channel👉 https://t.me/VneUrokaDev '

description_of_bot = 'Дорогой друг!\n\n Я так спешил, бежал, летел, старался успеть на Неделю иностранных языков🎓 и ' \
                     'все-таки ' \
                     'немного припозднился😒 \n\nНо…как говорится😉, _better late than never!!!_\n У меня есть ' \
                     'для тебя ' \
                     'сюрприз😍! '


def parse_user(message: types.Message):
    info = '{name} {surname} ({user_id})'. \
        format(name=message.from_user.first_name,
               surname=message.from_user.last_name,
               user_id=message.from_user.id)
    return info


def get_main_markup():
    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('Aviable games📲️', 'Leaders of games⚜️')
    main_markup.row('About🌚', 'About developer👨‍💻')
    return main_markup


def get_aviable_games_markup():
    markup = types.ReplyKeyboardMarkup()
    games = db_access.get_all_games()
    for g in games:
        markup.row(g.game_name)
    markup.row('Main menu📡')
    return markup


def get_task_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Get task🔄', 'Finish off the game😒')
    markup.row('Leaders of games⚜️', 'About🌚')
    return markup


def get_end_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Leaders of games⚜️', 'About🌚')
    markup.row('About developer👨‍💻')
    return markup


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Main menu📡')
def main_start(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    if user is None:
        bot.send_message(message.from_user.id, description_of_bot, parse_mode='Markdown',
                         reply_markup=get_main_markup())
    else:
        game_user = user.user_current_game
        count_level = db_access.get_tasks_of_game(game_user.game_name).count()
        if user.user_game_level is not count_level:
            bot.send_message(message.from_user.id, 'Are you in Game! 😎')
            bot.send_message(message.from_user.id, 'Click on the button to take action 📝',
                             reply_markup=get_task_markup())
        else:
            bot.send_message(message.from_user.id, description_of_bot, parse_mode='Markdown',
                             reply_markup=get_main_markup())


@bot.message_handler(func=lambda message: message.text == 'Aviable games📲️')
def aviable_games(message: types.Message):
    bot.send_message(message.from_user.id, 'List of aviable games: ')
    games = db_access.get_all_games()
    for g in games:
        bot.send_message(message.from_user.id, '{name}\n\n {desc}'
                         .format(name=g.game_name, desc=g.game_description))
    msg = bot.send_message(message.from_user.id, 'Select game', reply_markup=get_aviable_games_markup())
    bot.register_next_step_handler(msg, register_in_game)


def register_in_game(message: types.Message):
    if not message.text == 'Main menu📡':
        user = db_access.get_user(message.from_user.id)
        game = db_access.search_game(message.text)
        if user is None and game is not None:
            db_access.create_user(message.from_user.first_name, message.from_user.id,
                                  message.text, datetime.now())
            bot.send_message(message.from_user.id, 'You are in Game! 😎')
            bot.send_message(message.from_user.id, 'Click on the button to take action 📝',
                             reply_markup=get_task_markup())
        elif game is not None:
            is_user_end_game = db_access.is_user_finished_game(message.from_user.id, game)

            if is_user_end_game:
                bot.send_message(message.from_user.id, 'You are finished the game and save your result✅',
                                 reply_markup=get_main_markup())
            else:
                db_access.change_game_of_user(message.from_user.id, message.text)
                db_access.change_user_level(message.from_user.id, 0)
                bot.send_message(message.from_user.id, 'You are in Game {game}! 😎'.format(game=game.game_name))
                bot.send_message(message.from_user.id, 'Click on the button to take action 📝',
                                 reply_markup=get_task_markup())
        else:
            msg = bot.send_message(message.from_user.id, 'Game not found, please try again 👉')
            bot.register_next_step_handler(msg, register_in_game)

    else:
        bot.send_message(message.from_user.id, description_of_bot, reply_markup=get_main_markup(),
                         parse_mode='Markdown')


@bot.message_handler(func=lambda message: db_access.get_user(message.from_user.id) is not None
                     and message.text == 'Get task🔄')
def get_task(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    game = user.user_current_game
    count_level = db_access.get_tasks_of_game(game.game_name).count()
    level = db_access.get_user(message.from_user.id).user_game_level
    if level is not count_level:
        task = db_access.get_task(game.game_name, level + 1)
        bot.send_message(message.from_user.id, task.task_text)
        if task.task_photo is not None:
            photo = task.task_photo
            bot.send_photo(message.from_user.id, photo)
        msg = bot.send_message(message.from_user.id, 'Send me message, pls 😇',
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, check_answer)
    else:
        bot.send_message(message.from_user.id, 'You are complete the all tasks ✅, finish off the game')
        user = db_access.get_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Your total score: {score}'.format(score=user.user_all_score))


def check_answer(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    game = user.user_current_game
    count_level = db_access.get_tasks_of_game(game.game_name).count()
    user = db_access.get_user(message.from_user.id)
    level = user.user_game_level
    task_level = level + 1
    lower_message = message.text.lower()
    if user.user_tries is not 0:
        if level is not count_level:
            task = db_access.get_task(game.game_name, task_level)
            answer = task.task_answer
            if answer == lower_message:
                bot.send_message(message.from_user.id, 'That is right 😇, congratulations 🎓, you get {bonus} points'
                                 .format(bonus=task.task_bonus),
                                 reply_markup=get_task_markup())
                db_access.change_user_level(message.from_user.id, task_level)
                db_access.up_user_score(message.from_user.id, task.task_bonus)
                db_access.restore_user_tries(message.from_user.id)
            else:
                msg = bot.send_message(message.from_user.id, 'Sorry, answer is wrong. '
                                                             'You have {tries} tries for this quest(((. I am so sorry'
                                       .format(tries=user.user_tries - 1))
                db_access.down_user_tries(message.from_user.id, 1)
                bot.register_next_step_handler(msg, check_answer)
        else:
            bot.send_message(message.from_user.id, 'You are complete the all tasks ✅, finish off the game',
                             reply_markup=get_task_markup())
    else:
        bot.send_message(message.from_user.id, 'You have not got tries to answer',
                         reply_markup=get_task_markup())
        db_access.change_user_level(message.from_user.id, task_level)
        db_access.up_user_score(message.from_user.id, 0)
        db_access.restore_user_tries(message.from_user.id)


@bot.message_handler(func=lambda message: db_access.get_user(message.from_user.id) is not None
                     and message.text == 'Finish off the game😒')
def end_the_game(message: types.Message):
    result = db_access.end_user_playing(message.from_user.id, datetime.now())
    if result:
        user = db_access.get_user(message.from_user.id)
        db_access.create_user_finished_game(message.from_user.id, user.user_current_game)
        bot.send_message(message.from_user.id, 'You are finished the game and save your result✅',
                         reply_markup=get_main_markup())


@bot.message_handler(func=lambda message: message.text == 'Leaders of games⚜️')
def leaders_of_game(message: types.Message):
    if not message.text == 'Main menu📡':
        users = db_access.get_all_users_by_score()
        string = ''
        i = 0
        for u in users:
            i += 1
            if i is 1:
                string += 'Leader😎: {name} - {score} points⚜️\n'.format(name=u.user_name, score=u.user_all_score)
            else:
                string += '{name} - {score} points️\n'.format(name=u.user_name, score=u.user_all_score)
        bot.send_message(message.from_user.id, string)
    else:
        bot.send_message(message.from_user.id, description_of_bot,parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'About developer👨‍💻')
def about_developer(message: types.Message):
    bot.send_message(message.from_user.id, about_me)


@bot.message_handler(func=lambda message: message.text == 'About🌚')
def about_developer(message: types.Message):
    mes = 'Бот для «Недели иностранных языков» в МОУ Гимназии №2. Создан на основе бота с открытом исходным кодом, ' \
          'доступным по ссылке на странице GitHub: https://github.com/SkymanOne/quest-bot.\n\nПроект находиться в ' \
          'стадии активного развития. \n\nВсе пожелании вы можете оставить, связавшись с разработчиком по _кнопке_ ' \
          'ниже: '
    markup = types.ReplyKeyboardMarkup()
    markup.row('About developer👨‍💻', 'Main menu📡')
    bot.send_message(message.from_user.id, mes, parse_mode='Markdown', reply_markup=markup)


if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)
    server = Flask(__name__)


    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://quest-bot.herokuapp.com/" + token) # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5555)))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)

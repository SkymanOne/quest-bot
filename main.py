import telebot
from telebot import types
from models_pack import db_access, my_loging
from token_const import token
from datetime import datetime

bot = telebot.TeleBot(token)


about_me = 'German Nikolishin\n\nPython and .NET developer👨‍💻\nTelegram👉 @german_nikolishin\nGitHub👉 ' \
                  'https://github.com/SkymanOne\nVK👉 https://vk.com/german_it\nInst👉 ' \
                  'https://www.instagram.com/german.nikolishin/\nTelegram Channel👉 https://t.me/VneUrokaDev '


def parse_user(message: types.Message):
    info = '{name} {surname} ({user_id})'. \
        format(name=message.from_user.first_name,
               surname=message.from_user.last_name,
               user_id=message.from_user.id)
    return info


def get_main_markup():
    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('Aviable games📲️', 'Leaders of game⚜️')
    main_markup.row('About🌚', 'About developer')
    return main_markup


def get_aviable_games_markup():
    markup = types.ReplyKeyboardMarkup()
    games = db_access.get_all_games()
    for g in games:
        markup.row(g.game_name)
    return markup


def get_task_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Get task🔄', 'Finish off the game😒')
    markup.row('Leaders of game⚜️', 'About🌚')
    return markup


def get_end_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Leaders of game⚜️', 'About🌚')
    markup.row('About developer')
    return markup


@bot.message_handler(commands=['start'])
def main_start(message: types.Message):
    mes = 'Дорогой друг!\n\n Я так спешил, бежал, летел, старался успеть на Неделю иностранных языков🎓 и все-таки ' \
          'немного припозднился😒 \n\nНо…как говорится😉, <i>better late than never!!!</i>\n У меня есть для тебя ' \
          'сюрприз😍! '
    user = db_access.get_user(message.from_user.id)
    if user is None:
        msg = bot.send_message(message.from_user.id, mes, parse_mode='HTML', reply_markup=get_main_markup())
    else:
        game_user = user.user_current_game
        count_level = db_access.get_tasks_of_game(game_user.game_name).count()
        if user.user_game_level is not count_level:
            bot.send_message(message.from_user.id, 'Are you in Game! 😎')
            bot.send_message(message.from_user.id, 'Click on the button to take action 📝',
                             reply_markup=get_task_markup())


@bot.message_handler(func=lambda message: message.text == 'Aviable games📲️')
def aviable_games(message: types.Message):
    bot.send_message(message.from_user.id, 'List of aviable games: ')
    games = db_access.get_all_games()
    for g in games:
        bot.send_message(message.from_user.id, '{name}\n\n {desc}'
                         .format(name=g.game_name, desc=g.game_description))
    msg = bot.send_message(message.from_user.id, 'Select game', reply_markup=get_aviable_games_markup())
    bot.register_next_step_handler(msg, select_game)


# TODO: реализовать регистрацию в игре или отмену дейстуия
def select_game(message: types.Message):
    user = db_access.get_user(message.from_user.id)
    count_level = db_access.get_tasks_of_game('English videos').count()
    if user is None:
        game = db_access.search_game(message.text)
        if game is not None:
            string = game.game_description
            msg = bot.send_message(message.from_user.id, 'English videos\n\n' + string,
                                   reply_markup=get_main_markup())
    elif user.user_game_level is not count_level:
        bot.send_message(message.from_user.id, 'Are you in Game! 😎')
        bot.send_message(message.from_user.id, 'Click on the button to take action 📝',
                         reply_markup=get_task_markup())
    else:
        bot.send_message(message.from_user.id, 'You are finished the game and save your result✅',
                         reply_markup=get_end_markup())


@bot.message_handler(func=lambda message: db_access.get_user(message.from_user.id) is not None
                     and message.text == 'Get task🔄')
def get_task(message: types.Message):
    count_level = db_access.get_tasks_of_game('English videos').count()
    level = db_access.get_user(message.from_user.id).user_game_level
    if level is not count_level:
        task = db_access.get_task('English videos', level + 1)
        bot.send_message(message.from_user.id, task.task_text)
        msg = bot.send_message(message.from_user.id, 'Send me message, pls 😇')
        bot.register_next_step_handler(msg, check_answer)
    else:
        bot.send_message(message.from_user.id, 'You are complete the all tasks ✅, finish off the game')
        user = db_access.get_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Your total score: {score}'.format(score=user.user_all_score))


def check_answer(message: types.Message):
    count_level = db_access.get_tasks_of_game('English videos').count()
    user = db_access.get_user(message.from_user.id)
    level = user.user_game_level
    task_level = level + 1
    lower_message = message.text.lower()
    if user.user_tries is not 0:
        if level is not count_level:
            task = db_access.get_task('English videos', task_level)
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
                                       .format(tries=user.user_tries-1))
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
        bot.send_message(message.from_user.id, 'You are finished the game and save your result✅',
                         reply_markup=get_end_markup())


@bot.message_handler(func=lambda message: message.text == 'About developer')
def about_developer(message: types.Message):
    bot.send_message(message.from_user.id, about_me)


bot.polling(True)

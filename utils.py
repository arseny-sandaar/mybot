from emoji import emojize
from random import randint, choice
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def play_random_numbers(user_number):
    bot_number = randint(user_number-10,user_number+10)
    if user_number > bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}: you won!"
    elif user_number == bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}: it's a draw!"
    else:
        message = f"Your number is {user_number}, mine is {bot_number}: you lost!"
    return message

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])

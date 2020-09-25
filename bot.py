import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import (greet_user, planet_position, word_count, next_full_moon, 
                      guess_number, send_cat_picture, cities_game, user_coordinates, talk_to_me)

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME, 
        'password': settings.PROXY_PASSWORD}
    }

# def deEmojify(inputString):
#     return inputString.encode('ascii', 'ignore').decode('ascii')

def my_main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_position))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("next_full_moon",next_full_moon))
    dp.add_handler(CommandHandler("guess",guess_number))
    dp.add_handler(CommandHandler("cat",send_cat_picture))
    dp.add_handler(CommandHandler("cities", cities_game))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot has started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    my_main()

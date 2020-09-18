import logging
import ephem
from datetime import date

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME, 
        'password': settings.PROXY_PASSWORD}
    }


def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text('Привет, пользователь! Ты вызвал команду \n /start \
 \n /planet Planet - узнать созвездие планеты \
 \n /wordcount ''Ващ текст'' - узнать количество слов в тексте \
 \n /next_full_moon - узнать дату следующей полной луны')

# def talk_to_me(update, context):
#     user_text = update.message.text
#     print(user_text)
#     update.message.reply_text(user_text)

def planet_position(update,context):
    planet_name = update.message.text.split()[1]
    today = date.today().strftime("%Y/%m/%d")
    
    planeta = getattr(ephem,planet_name)
    constellation = ephem.constellation(planeta(today))
    update.message.reply_text(f"Положение {planet_name} на {today}: {constellation[1]}")

    # if planet_name == "Mars":
    #     mars = ephem.Mars(today)
    #     constellation = ephem.constellation(mars)
    #     update.message.reply_text(f"{planet_name} on {today}: {constellation}")
    # else:
    #     update.message.reply_text("Вызовите команду: /planet Planet")

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def word_count(update,context):

    user_text = update.message.text.split()[1:]
    if len(user_text) == 1:
        update.message.reply_text(f'В предложении {len(user_text)} слово')
    elif str(len(user_text))[:-1] == '1' and len(user_text) > 20:
        update.message.reply_text(f'В предложении {len(user_text)} слово')
    elif len(user_text) <= 4:
        update.message.reply_text(f'В предложении {len(user_text)} слова')
    elif int(str(len(user_text))[:-1]) <= 4 and len(user_text) > 20:
        update.message.reply_text(f'В предложении {len(user_text)} словa')
    elif len(user_text) == 0 or user_text == '':
        update.message.reply_text(f'В предложении нет слов. Введите после /start ВАШЕ ПРЕДЛОЖЕНИЕ.')
    else:
        update.message.reply_text(f'В предложении {len(user_text)} слов')

def next_full_moon(update,context):
    today = date.today().strftime("%Y-%m-%d")
    date_next_full_moon = ephem.next_full_moon(today)
    update.message.reply_text(f'Следующая полная луна {date_next_full_moon}')

def my_main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start",greet_user))
    # dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet",planet_position))
    dp.add_handler(CommandHandler("wordcount",word_count))
    dp.add_handler(CommandHandler("next_full_moon",next_full_moon))

    logging.info("Bot has started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    my_main()

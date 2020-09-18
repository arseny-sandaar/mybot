from datetime import date
import ephem
from emoji import emojize
from glob import glob
import logging
from random import randint, choice
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
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет, пользователь{context.user_data['emoji']}! Ты вызвал команду \n /start \
 \n /planet Planet - узнать созвездие планеты \
 \n /wordcount ''Ващ текст'' - узнать количество слов в тексте \
 \n /next_full_moon - узнать дату следующей полной луны \
 \n /guess number - игра угадать число большее, чем загаданное число бота")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text}{context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

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

    user_text = deEmojify(update.message.text).split()[1:]
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

def play_random_numbers(user_number):
    bot_number = randint(user_number-10,user_number+10)
    if user_number > bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}: you won!"
    elif user_number == bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}: it's a draw!"
    else:
        message = f"Your number is {user_number}, mine is {bot_number}: you lost!"
    return message

def guess_number(update,context):
    print(context.args)# .args stands for the content of the user text
    if context.args:
        try:# we first check wether the user enters an integer number
            user_number = int(context.args[0])# we convert it to an integer number
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):# in case the user types something different from a number weraise the error message for the user 
            message = "Enter an integer number."
    else:
        message = "Enter a number"
    update.message.reply_text(message)

def send_cat_picture(update,context):
    cat_photos_list = glob('images/cat*.jp*g')# with glob we get the files a corresponding names format 
    cat_pic_filename = choice(cat_photos_list)#
    chat_id = update.effective_chat.id#to get an id of the chat
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename,'rb'))# we need to point the id of the chat, 'rb' is read binary because the picture is a binary 

def my_main():
    mybot = Updater(settings.API_KEY, use_context = True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start",greet_user))
    dp.add_handler(CommandHandler("planet",planet_position))
    dp.add_handler(CommandHandler("wordcount",word_count))
    dp.add_handler(CommandHandler("next_full_moon",next_full_moon))
    dp.add_handler(CommandHandler("guess",guess_number))
    dp.add_handler(CommandHandler("cat",send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot has started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    my_main()

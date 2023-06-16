import telebot
from ozon.main import parse
import sqlite3
import config

bot = telebot.TeleBot(config.TG_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.last_name is None:
        name = message.from_user.first_name
    else:
        name = message.from_user.first_name + message.from_user.last_name
    send_message = f'Привет, <b>{name}</b>. Пришли мне запрос или фотографию товара, и я найду оптимальные варианты на Ozon.'
    bot.send_message(message.from_user.id, send_message, parse_mode='html')


@bot.message_handler()
def bot_message(message):
    bot.reply_to(message.from_user.id, "Помогите мне улучшить результаты поиска.")
    bot.send_message(message.from_user.id, "От какой цены начать поиск?")
    bot.send_message(message.from_user.id, "Идёт обработка информации, подождите!")
    parse(message.text)
    with open("ozon_result.csv","rb") as file:
        bot.send_document(message.from_user.id, file)


bot.polling(none_stop=True)
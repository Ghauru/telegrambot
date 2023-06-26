import telebot
from ozon.main import parse
import sqlite3
import config

sqlite_connect = sqlite3.connect('users.db', check_same_thread=False)
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE,' \
                      ' name TEXT, price INTEGER, price1 INTEGER, price2 INTEGER,' \
                      ' price3 INTEGER, price4 INTEGER, price5 INTEGER)'
cursor = sqlite_connect.cursor()
cursor.execute(sqlite_create_table)
cursor.close()

bot = telebot.TeleBot(config.TG_TOKEN)


def user_to_database(message):
    last_name = message.from_user.last_name
    if last_name is None:
        name = message.from_user.first_name
    else:
        name = message.from_user.first_name + message.from_user.last_name
    sql_insert_query = f'INSERT OR IGNORE INTO users(telegram_id, name, price, price1, price2, price3, price4, price5 )' \
                       f' VALUES("{message.from_user.id}", "{name}", {0}, {999999999}, {999999999}, {999999999}, ' \
                       f'{999999999}, {999999999})'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


def update_price(message):
    sql_insert_query = f'UPDATE users SET price = "{message.text}", price1 = "{999999999}", price2 = "{999999999}", ' \
                       f'price3 = "{999999999}", price4 = "{999999999}", price5 = "{999999999}" ' \
                       f'WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


@bot.message_handler(commands=['start'])
def start(message):
    user_to_database(message)
    cur = sqlite_connect.cursor()
    user_id = message.from_user.id
    res = cur.execute(f'SELECT name FROM users WHERE telegram_id="{user_id}"')
    name = res.fetchone()[0]
    cur.close()
    send_message = f'Привет, <b>{name}</b>. Пришли мне запрос или фотографию ' \
                   f'товара, и я найду оптимальные варианты на Ozon.'
    bot.send_message(message.from_user.id, send_message, parse_mode='html')


@bot.message_handler()
def bot_message(message):
    bot.reply_to(message, "Помогите мне улучшить результаты поиска.")
    msg = bot.reply_to(message, "От какой цены начать поиск?")
    bot.register_next_step_handler(msg, price)
    best_choice = parse(message.text, message.from_user.id)
    with open("ozon-result.csv", "rb") as file:
        bot.send_document(message.from_user.id, file)
    bot.send_message(message.from_user.id, "Лучшие 5 результатов: ")
    bot.send_photo(message.from_user.id, best_choice['photo'], caption=best_choice['title'] + '\nЦена ' + str(best_choice['price']) + '\n' + best_choice['url'])


def price(message):
    update_price(message)
    bot.send_message(message.from_user.id, "Идёт обработка информации, подождите!")


bot.polling(none_stop=True)
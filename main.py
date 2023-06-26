import telebot
from ozon.main import parse
import sqlite3
import config
import os
import shutil

sqlite_connect = sqlite3.connect('users.db', check_same_thread=False)
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE,' \
                      ' name TEXT, price INTEGER, price1 INTEGER, price2 INTEGER, ' \
                      'price3 INTEGER, price4 INTEGER, price5 INTEGER, photo_url1 TEXT, photo_url2 TEXT, ' \
                      'photo_url3 TEXT, photo_url4 TEXT, photo_url5 TEXT, name1 TEXT,' \
                      ' name2 TEXT, name3 TEXT, name4 TEXT, name5 TEXT,' \
                      ' link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, link5 TEXT)'
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
    sql_insert_query = f'INSERT OR IGNORE INTO users(telegram_id, name)' \
                       f' VALUES("{message.from_user.id}", "{name}")'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


def update_price(message):
    if message.text.lower() != 'нет':
        sql_insert_query = f'UPDATE users SET price = "{message.text}", price1 = "{999999999}", price2 = "{999999999}", ' \
                           f'price3 = "{999999999}", price4 = "{999999999}", price5 = "{999999999}",' \
                           f'photo_url1 = " ", photo_url2 = " ", photo_url3 = " ", photo_url4 = " ", photo_url5 = " ",' \
                           f'name1 = " ", name2 = " ", name3 = " ", name4 = " ", name5 = " ",' \
                           f'link1 = " ", link2 = " ", link3 = " ", link4 = " ", link5 = " "' \
                           f' WHERE telegram_id = "{message.from_user.id}"'

    else:
        sql_insert_query = f'UPDATE users SET price = "{0}", price1 = "{999999999}", price2 = "{999999999}", ' \
                           f'price3 = "{999999999}", price4 = "{999999999}", price5 = "{999999999}",' \
                           f'photo_url1 = " ", photo_url2 = " ", photo_url3 = " ", photo_url4 = " ", photo_url5 = " ",' \
                           f'name1 = " ", name2 = " ", name3 = " ", name4 = " ", name5 = " ",' \
                           f'link1 = " ", link2 = " ", link3 = " ", link4 = " ", link5 = " "' \
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
    try:
        os.makedirs(str(user_id) + '/products')
    except Exception:
        pass
    os.chdir("C:\\Users\\rules\\PycharmProjects\\telegrambot")
    res = cur.execute(f'SELECT name FROM users WHERE telegram_id="{user_id}"')
    name = res.fetchone()[0]
    cur.close()
    send_message = f'Привет, <b>{name}</b>. Пришли мне запрос или фотографию ' \
                   f'товара, и я найду оптимальные варианты на Ozon.'
    bot.send_message(message.chat.id, send_message, parse_mode='html')


@bot.message_handler()
def bot_message(message):
    user_id = message.from_user.id
    try:
        os.makedirs(str(user_id) + '/products')
    except Exception:
        pass
    os.chdir("C:\\Users\\rules\\PycharmProjects\\telegrambot")
    bot.reply_to(message, "Помогите мне улучшить результаты поиска.")
    msg = bot.reply_to(message, f"От какой цены начать поиск? Отправьте <b>Нет</b>, если хотите не учитывать цену", parse_mode='html')
    bot.register_next_step_handler(msg, price)
    parse(message.text, message.from_user.id)
    bot.send_message(message.chat.id, "Лучшие 5 результатов: ")
    cur = sqlite_connect.cursor()
    cur.execute(f'SELECT photo_url1 FROM users WHERE telegram_id = "{user_id}"')
    photo1 = cur.fetchone()[0]
    cur.execute(f'SELECT photo_url2 FROM users WHERE telegram_id = "{user_id}"')
    photo2 = cur.fetchone()[0]
    cur.execute(f'SELECT photo_url3 FROM users WHERE telegram_id = "{user_id}"')
    photo3 = cur.fetchone()[0]
    cur.execute(f'SELECT photo_url4 FROM users WHERE telegram_id = "{user_id}"')
    photo4 = cur.fetchone()[0]
    cur.execute(f'SELECT photo_url5 FROM users WHERE telegram_id = "{user_id}"')
    photo5 = cur.fetchone()[0]
    cur.execute(f'SELECT link1 FROM users WHERE telegram_id = "{user_id}"')
    link1 = cur.fetchone()[0]
    cur.execute(f'SELECT link2 FROM users WHERE telegram_id = "{user_id}"')
    link2 = cur.fetchone()[0]
    cur.execute(f'SELECT link3 FROM users WHERE telegram_id = "{user_id}"')
    link3 = cur.fetchone()[0]
    cur.execute(f'SELECT link4 FROM users WHERE telegram_id = "{user_id}"')
    link4 = cur.fetchone()[0]
    cur.execute(f'SELECT link5 FROM users WHERE telegram_id = "{user_id}"')
    link5 = cur.fetchone()[0]
    cur.execute(f'SELECT name1 FROM users WHERE telegram_id = "{user_id}"')
    name1 = cur.fetchone()[0]
    cur.execute(f'SELECT name2 FROM users WHERE telegram_id = "{user_id}"')
    name2 = cur.fetchone()[0]
    cur.execute(f'SELECT name3 FROM users WHERE telegram_id = "{user_id}"')
    name3 = cur.fetchone()[0]
    cur.execute(f'SELECT name4 FROM users WHERE telegram_id = "{user_id}"')
    name4 = cur.fetchone()[0]
    cur.execute(f'SELECT name5 FROM users WHERE telegram_id = "{user_id}"')
    name5 = cur.fetchone()[0]
    cur.execute(f'SELECT price1 FROM users WHERE telegram_id = "{user_id}"')
    price1 = cur.fetchone()[0]
    cur.execute(f'SELECT price2 FROM users WHERE telegram_id = "{user_id}"')
    price2 = cur.fetchone()[0]
    cur.execute(f'SELECT price3 FROM users WHERE telegram_id = "{user_id}"')
    price3 = cur.fetchone()[0]
    cur.execute(f'SELECT price4 FROM users WHERE telegram_id = "{user_id}"')
    price4 = cur.fetchone()[0]
    cur.execute(f'SELECT price5 FROM users WHERE telegram_id = "{user_id}"')
    price5 = cur.fetchone()[0]
    photo_list = [photo1, photo2, photo3, photo4, photo5]
    print(''.join(photo_list))
    if not (''.join(photo_list).isspace()):
        media = []
        for photo in photo_list:
            media.append(telebot.types.InputMediaPhoto(photo))
        bot.send_media_group(chat_id=message.chat.id, media=media)
        text = '1) {}. {} ({}₽)\n2) {}. {} ({}₽)\n3) {}. {} ({}₽)\n4) {}. {} ({}₽)\n 5) {}. {} ({}₽)\n'.format(name1,
                link1, str(price1), name2, link2, str(price2), name3, link3, str(price3), name4, link4, str(price4),
                name5, link5, str(price5))
        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
        bot.send_message(message.chat.id, 'CSV файл с остальными результатами:')
        with open(message.from_user.id + "/ozon_result.csv", "rb") as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'Вы ввели слишком большую начальную цену для поиска, либо таких товаров не нашлось')
    cur.close()
    shutil.rmtree(str(user_id))


def price(message):
    update_price(message)
    bot.send_message(message.chat.id, "Идёт обработка информации, подождите!")


bot.polling(none_stop=True)

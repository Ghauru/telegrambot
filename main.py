import sqlite3
import config
from class_bot import Bot
import asyncio
import nest_asyncio


sqlite_connect = sqlite3.connect('users.db', check_same_thread=False)
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE,' \
                      ' name TEXT, price INTEGER, price1 INTEGER, price2 INTEGER, ' \
                      'price3 INTEGER, price4 INTEGER, price5 INTEGER, photo_url1 TEXT, photo_url2 TEXT, ' \
                      'photo_url3 TEXT, photo_url4 TEXT, photo_url5 TEXT, name1 TEXT,' \
                      ' name2 TEXT, name3 TEXT, name4 TEXT, name5 TEXT,' \
                      ' link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, link5 TEXT, search TEXT)'
cursor = sqlite_connect.cursor()
cursor.execute(sqlite_create_table)
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS url_index ON users (link1, link2, link3, link4, link5)')
cursor.close()


async def start_bot():
    bot = Bot(token=config.TG_TOKEN)
    await bot.start()


nest_asyncio.apply()
asyncio.run(start_bot())

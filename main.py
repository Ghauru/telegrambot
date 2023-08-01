import aiogram
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from ozon.main import process_requests
import sqlite3
import config
import os
import shutil
import requests
import uuid
import asyncio

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
storage = MemoryStorage()


async def user_to_database(message):
    search = ' '
    last_name = message.from_user.last_name
    if last_name is None:
        name = message.from_user.first_name
    else:
        name = message.from_user.first_name + message.from_user.last_name
    sql_insert_query = f'INSERT OR IGNORE INTO users(telegram_id, name, search)' \
                       f' VALUES("{message.from_user.id}", "{name}", "{search}")'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


async def update_search(message):
    sql_insert_query = f'UPDATE users SET search = "{message.text}" WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


async def update_price(message):
    new_links = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    if message.text.isnumeric():
        text = int(message.text)
        sql_insert_query = f'UPDATE users SET price = "{text}", price1 = "{999999999}", price2 = "{999999999}", ' \
                           f'price3 = "{999999999}", price4 = "{999999999}", price5 = "{999999999}",' \
                           f'photo_url1 = " ", photo_url2 = " ", photo_url3 = " ", photo_url4 = " ", photo_url5 = " ",' \
                           f'name1 = " ", name2 = " ", name3 = " ", name4 = " ", name5 = " ",' \
                           f'link1 = "{new_links[0]}", link2 = "{new_links[1]}", link3 = "{new_links[2]}", ' \
                           f'link4 = "{new_links[3]}", link5 = "{new_links[4]}"' \
                           f'WHERE telegram_id = "{message.from_user.id}"'
    else:
        sql_insert_query = f'UPDATE users SET price = "{0}", price1 = "{999999999}", price2 = "{999999999}", ' \
                           f'price3 = "{999999999}", price4 = "{999999999}", price5 = "{999999999}",' \
                           f'photo_url1 = " ", photo_url2 = " ", photo_url3 = " ", photo_url4 = " ", photo_url5 = " ",' \
                           f'name1 = " ", name2 = " ", name3 = " ", name4 = " ", name5 = " ",' \
                           f'link1 = "{new_links[0]}", link2 = "{new_links[1]}", link3 = "{new_links[2]}",' \
                           f' link4 = "{new_links[3]}", link5 = "{new_links[4]}"' \
                           f'WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


class Form(StatesGroup):
    text = State()


class Bot:
    def __init__(self, token):
        self.bot = aiogram.Bot(token)
        self.dp = aiogram.Dispatcher(self.bot, storage=storage)

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await user_to_database(message)
            cur = sqlite_connect.cursor()
            user_id = message.from_user.id
            res = cur.execute(f'SELECT name FROM users WHERE telegram_id="{user_id}"')
            name = res.fetchone()[0]
            cur.close()
            send_message = f'Привет, <b>{name}</b>. Пришли мне запрос' \
                           f'товара, и я найду оптимальные варианты на Ozon.'
            await self.send_message(message.chat.id, send_message, parse_mode='html')

        @self.dp.message_handler()
        async def bot_message(message: types.Message):
            user_id = message.from_user.id
            try:
                os.makedirs(str(user_id) + '/products')
                os.makedirs(str(user_id) + '/pages')
            except:
                pass
            os.chdir("C:\\Users\\rules\\PycharmProjects\\telegrambot")
            await self.send_message(message.chat.id, "Помогите мне улучшить результаты поиска.")
            await self.send_message(message.chat.id, f"От какой цены начать поиск? Отправьте <b>Нет</b>,"
                                                     f" если хотите не учитывать цену."
                               f" Учтите, что без указания цены поиск может быть неточным", parse_mode='html')
            await update_search(message)
            await Form.text.set()

        @self.dp.message_handler(state=Form.text)
        async def bot_cont_message(message: types.Message, state: FSMContext):
            user_id = message.from_user.id
            cur = sqlite_connect.cursor()
            res = cur.execute(f'SELECT search FROM users WHERE telegram_id="{user_id}"')
            text = res.fetchone()[0]
            cur.close()
            await state.finish()
            await self.price(message)
            url = f'https://api.telegram.org/bot{config.TG_TOKEN}/getUpdates'
            timeout = 300

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
            except requests.exceptions.ReadTimeout as e:
                print(f"Ошибка чтения данных: {e}")
            except requests.exceptions.HTTPError as e:
                print(f"Ошибка HTTP: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса: {e}")
            else:
                print(response.json())
            await process_requests(text, message.from_user.id)
            await self.send_message(message.chat.id, "Лучшие 5 результатов: ")
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
            if not (''.join(photo_list).isspace()):
                media = []
                for photo in photo_list:
                    media.append(aiogram.types.InputMediaPhoto(photo))
                await self.send_media_group(chat_id=message.chat.id, media=media)
                text = '1) {}. {} ({}₽)\n2) {}. {} ({}₽)\n3) {}. {} ({}₽)\n4) {}. {} ({}₽)\n 5) {}. {} ({}₽)\n'.format(
                    name1,
                    link1,
                    str(price1),
                    name2,
                    link2,
                    str(price2),
                    name3,
                    link3,
                    str(price3),
                    name4,
                    link4,
                    str(price4),
                    name5,
                    link5,
                    str(price5))
                await self.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
                await self.send_message(message.chat.id, 'CSV файл со всеми результатами:')
                with open(str(user_id) + "/ozon_result.csv", "rb") as file:
                    await self.send_document(message.chat.id, file)
            else:
                await self.send_message(message.chat.id, 'Вы ввели слишком большую начальную цену для поиска,'
                                                         ' либо таких товаров не нашлось')
            cur.close()
            shutil.rmtree(str(user_id))

    async def send_message(self, chat_id, text, reply_to_message_id=None, parse_mode=None):
        await self.bot.send_message(chat_id, text, reply_to_message_id=reply_to_message_id, parse_mode=parse_mode)

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.dp.start_polling())
        loop.run_forever()

    async def send_media_group(self, chat_id, media):
        await self.bot.send_media_group(chat_id, media)

    async def send_document(self, chat_id, document):
        await self.bot.send_document(chat_id, document)

    async def price(self, message: types.Message):
        await update_price(message)
        await self.send_message(message.chat.id, "Идёт обработка информации, подождите!")


# Пример использования:
bot = Bot(token=config.TG_TOKEN)
bot.start()

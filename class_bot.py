import uuid
import sqlite3
from ozon.main import parse


class Bot:

    def __init__(self, message):
        self.message = message
        self.sqlite_connect = sqlite3.connect('users.db', check_same_thread=False)





    def bot_parse(self):
        msg = self.message
        parse(msg.text, msg.from_user.id)

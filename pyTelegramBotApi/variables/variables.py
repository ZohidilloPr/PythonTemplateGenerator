ENV="""TOKEN="<telegram bot token>"
DB_NAME="<example: postgres>"
DB_USER="<example: postgres>"
DB_PASS="<example: 123465>"
DB_HOST="localhost"
"""

MAIN="""from config.loader import bot, db
db.making_users_table() # make users table when bot start to run

import handlers



if __name__ == "__main__":
    print("Bot is running....")
    bot.polling() # for bot in developping time
    # bot.infinity_polling # for bot in running in real server
"""
INLINE_MARKUB = """from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def help_btn():
    markub = InlineKeyboardMarkup()
    markub.add(InlineKeyboardButton("dasturchi", url="https://t.me/ZohidilloTurgunov/"))
    return markub
"""
REPLY_MARKUB = """from telebot.types import ReplyKeyboardMarkup, KeyboardButton"""

CALLBACK_QUERY = """from telebot.types import CallbackQuery

from config.loader import bot, db
"""

TEXT_HANDLER="""from telebot.types import Message

# local variables
from config.loader import bot, db
"""

COMMANDS = """from telebot.types import Message

# local variables
from config.loader import bot, db
from keyboards.inline_markup import help_btn


# start coding
@bot.message_handler(commands=["start", "help"])
def reaction_commands(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "/start":
        check = db.check_user_exists(user_id)
        if check:
            if user_id in db.get_admins_telegram_id():
                bot.send_message(chat_id, "Assalom Aleykum Admin")
            elif user_id not in db.get_admins_telegram_id():
                bot.send_message(chat_id, "Assalom Aleykum")
        else: 
            bot.send_message(chat_id, "Assalomu Aleykum Iltimos ro'yhatdan o'ting")
    elif message.text == "/help":
        bot.send_message(chat_id, "Dasturchi bilan bog'lanish", reply_markup=help_btn())
"""

DATABASE = '''import psycopg2

class Database:
    def __init__(self, db_name, db_user, db_pass, db_host):
        self.connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_pass,
            host=db_host
        )

    def maneger(self, sql, commit: bool=False, fetchall: bool=False, fetchone: bool=False):
        with self.connection as db:
            cursor = db.cursor()
            cursor.execute(sql)
            if commit:
               return db.commit()
            elif fetchall:
                return cursor.fetchall()
            elif fetchone:
                return cursor.fetchone()
    
    # making tables
    def making_users_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                telegram_id BIGSERIAL PRIMARY KEY,
                f_name VARCHAR (50),
                l_name VARCHAR (100),
                username VARCHAR (30)),
                is_admin BOOLEAN DEFAULT FALSE,
                register_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            ) 
        """
        self.maneger(sql, commit=True)
    
    def insert_users_table(self, telegram_id, f_name, l_name, username):
        sql = """
            INSERT INTO users (telegram_id, f_name, l_name, username)
            VALUES ('%i', '%s', '%s', "%s")
        """ % (telegram_id, f_name, l_name, username)
        self.maneger(sql, commit=True)
    

    def get_user_from_users(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id=%i" % telegram_id
        return self.maneger(sql, fetchone=True)
    

    def get_admins_telegram_id(self):
        sql = """ SELECT telegram_id FROM users WHERE is_admin=TRUE; """
        return [admin[0] for admin in self.maneger(sql, fetchall=True)]
    
    def check_user_exists(self, telegram_id):
        sql = """ SELECT * FROM users WHERE telegram_id=%i; """ % telegram_id
        return True if self.maneger(sql, fetchone=True) is not None else False
'''

LOADER = """from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

# local variables
from database import Database
from settings import (TOKEN, DB_NAME, DB_USER, DB_PASS, DB_HOST) 

# settings bot
bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(custom_filters.StateFilter(bot))

# settings database
db = Database(DB_NAME, DB_USER, DB_PASS, DB_HOST)

# commands menu for users
bot.set_my_commands(commands=[
    BotCommand("start", "Botni qayta ishga tushirish"),
    BotCommand("help", "Yordam"),
    # your commands for menu
])
"""
SETTINGS = """from decouple import config

TOKEN = config("TOKEN")
DB_NAME=config("DB_NAME")
DB_USER=config("DB_USER")
DB_PASS=config("DB_PASS")
DB_HOST=config("DB_HOST")
"""
STATES="""from telebot.handler_backends import State, StatesGroup

class RegisterUserState(StatesGroup):
    f_name = State()
    l_name = State()
    username = State()
    save = State()
"""
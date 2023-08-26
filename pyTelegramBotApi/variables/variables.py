ENV="""TOKEN="<telegram bot token>"
DB_NAME="<example: postgres>"
DB_USER="<example: postgres>"
DB_PASS="<example: 123465>"
DB_HOST="localhost"
GROUP_ID=-12312312123
POSTGRES_ENGINE="postgresql://<db_user>:<db_pass>@localhost:5432/<db_name>"
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
REPLY_MARKUB = """from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config.loader import db
"""

CALLBACK_QUERY = """from telebot.types import CallbackQuery

from config.loader import bot, db

# globals
ADMINS = db.get_admins_telegram_id()

def requared_admin(func):
    def methods(call: CallbackQuery):
        if call.chat.id in ADMINS:
            func(call)
        else:
            bot.send_call(call.chat.id, "Bu ammallar faqat adminlar uchun!!!")
    return methods  

"""

TEXT_HANDLER="""from telebot.types import Message

# local variables
from config.loader import bot, db


# globals
ADMINS = db.get_admins_telegram_id()

def requared_admin(func):
    def methods(message: Message):
        if message.chat.id in ADMINS:
            func(message)
        else:
            bot.send_message(message.chat.id, "Bu ammallar faqat adminlar uchun!!!")
    return methods


@requared_admin
@bot.massage_handler(context_type=["text"])
def reaction_test(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, message.text)

"""

COMMANDS = """from telebot.types import Message

# local variables
from config.loader import bot, db
from keyboards.inline_markup import help_btn


# start coding
@bot.message_handler(commands=["start", "help", "my_id])
def reaction_commands(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if message.text == "/start":
        ADMINS = db.get_admins_telegram_id()
        check = db.check_user_exists(user_id)
        if check:
            if user_id in ADMINS:
                bot.send_message(chat_id, "Assalom Aleykum Admin")
            elif user_id not in ADMINS:
                bot.send_message(chat_id, "Assalom Aleykum Bot ishga tushdi.")
        else:
            telegram_id = int(user_id)
            f_name = message.from_user.first_name
            l_name = message.from_user.last_name
            username = message.from_user.username
            db.insert_users_table(telegram_id, f_name, l_name, username)
            bot.send_message(chat_id, "Assalomu Alykum Bot ishga tushdi.")
    
    elif message.text == "/help":
        bot.send_message(chat_id, "Dasturchi bilan bog'lanish", reply_markup=help_btn())
    
    elif message.text == "/my_id":
        bot.send_message(chat_id, f"UserID: {chat_id}")
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
                username VARCHAR (50),
                is_admin BOOLEAN DEFAULT FALSE,
                register_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            ) 
        """
        self.maneger(sql, commit=True)
    

    def insert_users_table(self, telegram_id, f_name, l_name, username):
        sql = """
            INSERT INTO users (telegram_id, f_name, l_name, username)
            VALUES ('%i', '%s', '%s', '%s') ON CONFLICT DO NOTHING
        """ % (telegram_id, f_name, l_name, username)
        self.maneger(sql, commit=True)


    def set_admins(self, admin_id: int):
        sql = "UPDATE users SET is_admin=TRUE WHERE telegram_id='%i'" % admin_id
        self.maneger(sql, commit=True)

    
    def set_default_admins(self, admins: list):
        for user in admins:
            sql = f"UPDATE users SET is_admin=TRUE WHERE telegram_id={user};"
            self.maneger(sql, commit=True)


    def get_user_from_users(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id=%i" % telegram_id
        return self.maneger(sql, fetchone=True)
    

    def get_admins_telegram_id(self):
        sql = """ SELECT telegram_id FROM users WHERE is_admin=TRUE; """
        return [int(admin[0]) for admin in self.maneger(sql, fetchall=True)]
    
    
    def check_user_exists(self, telegram_id):
        sql = """ SELECT * FROM users WHERE telegram_id=%i; """ % telegram_id
        return True if self.maneger(sql, fetchone=True) is not None else False
'''

LOADER = """from telebot.types import BotCommand
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

# local variables
from .database import Database
from .settings import (TOKEN, DB_NAME, DB_USER, DB_PASS, DB_HOST) 

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
GROUP_ID=config("GROUP_ID")

"""
STATES="""from telebot.handler_backends import State, StatesGroup

class SomeThingState(StatesGroup):
    example = State()

"""
TEST = """import re
import os
from pathlib import Path
from pprint import pprint
from config.loader import db
from config.settings import *
from datetime import datetime
"""
SERVICE="""
[Unit]
Description=descripion of telegram bot
After=network.target

[Service]
User={vps_user}
WorkingDirectory=/home/{vps_user}/{bot_folder}
ExecStart=/home/{vps_user}/{bot_folder}/online/bin/python main.py'
Restart=always

[Install]
WantedBy=multi-user.target
"""
RESTART = """import os
os.system('sudo systemctl restart {service_name}.service')
"""
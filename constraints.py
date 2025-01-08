import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db import Database

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN', '')
USER_ID = os.getenv('USER_ID', '')
bot = Bot(TOKEN)
dp = Dispatcher()
db = Database()

UPDATES = 'updates'
SCHEDULE = 'schedule'

USD_FIELDS = {
    'Белый': ('tn_text_1729075851837', 'tn_text_1729075851839'),
    'Синий': ('tn_text_1680795335003', 'tn_text_1680795214553')
}
SEND_MESSAGE = ('💲<i>{currency[0]}</i>💲\n'.center(20, '_') +
                ('{currency[1][0]}' + ' ' * 5 + '{currency[1][1]}').center(20))

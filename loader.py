from aiogram import Bot, Dispatcher
from data import config
from baza.sqlite import Database
from aiogram.enums import ParseMode

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN


bot = Bot(TOKEN)
db = Database(path_to_db="main.db")
dp = Dispatcher()
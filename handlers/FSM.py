import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.fsm.state import State, StatesGroup

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)


class FSMFillForm(StatesGroup):

    fill_name = State()
    fill_mistake = State()
    fill_description = State()
    fill_level = State()
    fill_place = State()
    upload_photo = State()

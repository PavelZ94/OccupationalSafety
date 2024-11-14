import pytest
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Update, Message
#from aiogram.utils import executor
from unittest.mock import AsyncMock

from django.core.files.storage import storages

from handlers.user_handlers import process_start_command, router
from lexicon.lexicon import (start_command_text,
                              help_command_text,
                              enter_name_text,
                              default_cancel_text,
                              cancel_text)

class MockBot:
    def __init__(self):
        self.sent_messages = []

    async def answer(self, message: str):
        self.sent_messages.append(message)

router = Router()


@pytest.fixture
async def mock_bot():
    return MockBot()

#@pytest.fixture
#def bot():
#    BOT_TOKEN = os.getenv('BOT_TOKEN')
#    return Bot(BOT_TOKEN)


#@pytest.fixture
#def dispatcher(bot):
#    storage = MemoryStorage()
#    dp = Dispatcher(storage=storage)
#    dp.bot = bot
#    return dp
@pytest.fixture
async def dispatcher(mock_bot):
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.bot = mock_bot
    dp.include_router(router)
    return dp


@pytest.mark.asyncio
async def test_start_handler(dispatcher, mock_bot):
    message = types.Message(
        message_id=1,
        from_user=types.User(id=123, is_bot=False, first_name='Test'),
        chat=types.Chat(id=123, type='private'),
        date='2023-01-01T00:00:00Z',
        text='/start'
    )

    #dispatcher.message.register(process_start_command, Command(commands=['start']))

    update = Update(update_id=1, message=message)

    await dispatcher._process_update(mock_bot, update)

    assert len(mock_bot.sent_messages) == 1
    assert mock_bot.sent_messages[0] == start_command_text
    #expected_response = start_command_text
    #assert message.text == expected_response

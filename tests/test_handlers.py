import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from django.db.models.fields import return_None
from jedi.debug import speed

from handlers.FSM import FSMFillForm
from aiogram.fsm.state import default_state
from handlers.user_handlers import process_cancel_command_state, process_name_sent
#from handlers.warning_handlers import
from lexicon.lexicon import (cancel_text,
                             accepted_name_text)
from database.database import insert_user_name


@pytest.fixture
def bot():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    return Bot(BOT_TOKEN)


@pytest.fixture
def dispatcher(bot):
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    return dp


@pytest.fixture
def mock_message():
    message = MagicMock(spec=Message)
    message.answer = MagicMock()
    return message


@pytest.mark.asyncio
async def test_process_cancel_command_state(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_message.chat = mock_chat
    mock_message.text = '/cancel'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.fill_name

    await process_cancel_command_state(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=cancel_text)

    mock_state.clear.assert_called_once()


@pytest.mark.asyncio
async def test_process_name_sent(mock_message):
    mock_message = MagicMock()
    mock_state = MagicMock(spec=FSMContext)

    mock_message.from_user.id = 12345
    mock_message.text = 'Test'
    mock_message.answer = AsyncMock()

    with patch('database.database.insert_user_name', new_callable=AsyncMock) as insert_user_name_mock:
        insert_user_name_mock.return_value = 1

        await process_name_sent(mock_message, mock_state)

        insert_user_name_mock.assert_called_once_with(mock_message.from_user.id, mock_message.text)

        mock_state.update_data.assert_called_once_with(name=mock_message.text, id=1)

        mock_message.answer.assert_called_once_with(text=accepted_name_text)

        mock_state.set_state.assert_called_once_with(FSMFillForm.fill_mistake)

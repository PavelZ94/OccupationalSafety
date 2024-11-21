import pytest
from unittest.mock import AsyncMock, MagicMock
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.FSM import FSMFillForm
from handlers.user_handlers import (process_cancel_command_state,
                                    process_name_sent)
from lexicon.lexicon import (cancel_text,
                             accepted_name_text)


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
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_user = MagicMock()
    mock_user.id = 54321
    mock_message.from_user = mock_user

    mock_message.chat = mock_chat
    mock_message.text = 'Test'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.fill_name

    await process_name_sent(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=accepted_name_text)
    mock_state.set_state.assert_called_once_with(FSMFillForm.fill_mistake)

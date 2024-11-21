import pytest
from unittest.mock import AsyncMock, MagicMock
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.FSM import FSMFillForm
from handlers.user_handlers import (process_start_command,
                                    process_help_command,
                                    process_mistake_command)
from handlers.warning_handlers import process_cancel_command
from lexicon.lexicon import (start_command_text,
                             help_command_text,
                             enter_name_text,
                             default_cancel_text)


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
async def test_process_start_command(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_message.chat = mock_chat
    mock_message.text = '/start'
    mock_message.answer = AsyncMock()

    await process_start_command(mock_message)

    mock_message.answer.assert_called_once_with(text=start_command_text)


@pytest.mark.asyncio
async def test_process_help_command(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_message.chat = mock_chat
    mock_message.text = '/help'
    mock_message.answer = AsyncMock()

    await process_help_command(mock_message)

    mock_message.answer.assert_called_once_with(text=help_command_text)


@pytest.mark.asyncio
async def test_process_cancel_command(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_message.chat = mock_chat
    mock_message.text = '/cancel'
    mock_message.answer = AsyncMock()

    await process_cancel_command(mock_message)
    mock_message.answer.assert_called_once_with(text=default_cancel_text)


@pytest.mark.asyncio
async def test_process_mistake_command(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_message.chat = mock_chat
    mock_message.text = '/mistake'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    await process_mistake_command(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=enter_name_text)

    mock_state.set_state.assert_called_once_with(FSMFillForm.fill_name)

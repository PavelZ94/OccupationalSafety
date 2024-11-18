import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.FSM import FSMFillForm
from aiogram.fsm.state import default_state
from handlers.user_handlers import (process_cancel_command_state,
                                    process_name_sent,
                                    process_mistake_command,
                                    process_mistake_sent,
                                    process_description_sent,
                                    process_level_press,
                                    process_place_sent,
                                    process_photo_sent)
#from handlers.warning_handlers import
from lexicon.lexicon import (cancel_text,
                             accepted_name_text,
                             accepted_mistake_text,
                             accepted_description_text,
                             accepted_level_text,
                             accepted_place_text,
                             accepted_request_text)


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


@pytest.mark.asyncio
async def test_process_mistake_sent(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_user = MagicMock()
    mock_user.id = 54321
    mock_message.from_user = mock_user

    mock_message.chat = mock_chat
    mock_message.text = 'Valid brief information'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.fill_mistake

    await process_mistake_sent(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=accepted_mistake_text)
    mock_state.set_state.assert_called_once_with(FSMFillForm.fill_description)


@pytest.mark.asyncio
async def test_process_description_sent(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_user = MagicMock()
    mock_user.id = 54321
    mock_message.from_user = mock_user

    mock_message.chat = mock_chat
    mock_message.text = 'Valid detailed description'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.fill_description

    await process_description_sent(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=accepted_description_text)
    mock_state.set_state.assert_called_once_with(FSMFillForm.fill_level)


@pytest.mark.asyncio
async def test_process_level_press(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_user = MagicMock()
    mock_user.id = 54321
    mock_message.from_user = mock_user

    mock_message.chat = mock_chat
    mock_message.text = 'medium'
    mock_message.answer = AsyncMock()

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.fill_level

    await process_level_press(mock_message, mock_state)
    mock_message.answer.assert_called_once_with(text=accepted_level_text)
    mock_state.set_state.assert_called_once_with(FSMFillForm.fill_place)


@pytest.mark.asyncio
async def test_process_photo_sent(mock_message):
    mock_chat = MagicMock()
    mock_chat.id = 12345

    mock_user = MagicMock()
    mock_user.id = 54321
    mock_message.from_user = mock_user

    mock_message.chat = mock_chat
    mock_message.answer = AsyncMock()

    mock_file = MagicMock()
    mock_file.file_path = 'mock/file/path.jpg'

    mock_message.bot.get_file = AsyncMock(return_value=mock_file)

    mock_state = MagicMock(spec=FSMContext)

    mock_state.get_state.return_value = FSMFillForm.upload_photo

    await process_place_sent(mock_message, mock_state, mock_file)
    mock_message.answer.assert_called_once_with(text=accepted_request_text)
    mock_state.clear.assert_called_once()
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import (default_cancel_text,
                             warning_name_text,
                             warning_mistake_text,
                             warning_description_text,
                             warning_level_text,
                             warning_place_text,
                             warning_photo_text)
from handlers.FSM import FSMFillForm


router = Router()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    """
    Handler responding to an attempt to execute a cancel command
    from the default state.
    It shows a message, that there is nothing to cancel in default state.

    Args:
        message: '/cancel' command.

    State:
        Default state.
    """
    await message.answer(text=default_cancel_text)


@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    """
    Message that appears if the name does not pass the validity check.
    It shows next options of using the bot.

    Args:
        message: not valid username.

    Previous state: fill name state.
    Next state: fill name state.
    """
    await message.answer(text=warning_name_text)


@router.message(StateFilter(FSMFillForm.fill_mistake))
async def warning_not_mistake(message: Message):
    """
    Message that appears if the mistake does not pass the validity check.
    It shows next options of using the bot.

    Args:
        message: not valid mistake.

    Previous state: fill mistake state.
    Next state: fill mistake state.
    """
    await message.answer(text=warning_mistake_text)


@router.message(StateFilter(FSMFillForm.fill_description))
async def warning_not_description(message: Message):
    """
    Message that appears if description does not pass the validity check.
    It shows next options of using the bot.

    Args:
        message: not valid description.

    Previous state: fill description state.
    Next state: fill description state.
    """
    await message.answer(text=warning_description_text)


@router.message(StateFilter(FSMFillForm.fill_level))
async def warning_not_level(message: Message):
    """
    Message that appears if the user does not use inline buttons
    or enters invalid values.
    It shows next options of using the bot.

    Args:
        message: not valid level chosen.

    Previous state: fill level state.
    Next state: fill level state.
    """
    await message.answer(text=warning_level_text)


@router.message(StateFilter(FSMFillForm.fill_place))
async def warning_not_place(message: Message):
    """
    Message that appears if violation place does not pass the validity check.
    It shows next options of using the bot.

    Args:
        message: not valid place.

    Previous state: fill place state.
    Next state: fill place state.
    """
    await message.answer(text=warning_place_text)


@router.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
    """
    Message that appears if the user sends something instead of a photo.
    It shows next options of using the bot.

    Args:
        message: not valid photo.

    Previous state: upload photo state.
    Next state: upload photo state.
    """
    await message.answer(text=warning_photo_text)

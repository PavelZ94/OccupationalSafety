import os
from dotenv import load_dotenv
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           Message,
                           PhotoSize)
from database.database import (insert_user_name,
                               insert_mistake,
                               insert_level,
                               insert_description,
                               insert_place,
                               insert_photo,
                               get_user_id)
from lexicon.lexicon import (start_command_text,
                             help_command_text,
                             cancel_text,
                             enter_name_text,
                             accepted_name_text,
                             accepted_mistake_text,
                             accepted_description_text,
                             accepted_level_text,
                             accepted_place_text,
                             accepted_request_text)

router = Router()

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


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """
    Handler processing the start command.
    It shows next options of using bot.

    Args:
        message: '/start' command.
    State:
        It is called from the default state.
    """
    await message.answer(text=start_command_text)


@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    """
    Handler processing the help command.
    Is shows definition of 'Near-miss'.

    Args:
        message: '/help' command.
    State:
        Default state.
    """
    await message.answer(text=help_command_text)


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    """
    Handler responding to an attempt to execute a cancel command
    from all states except default state.
    It shows next options of using the bot.

    Args:
        message: '/cancel' command.
        state: all states except default state.

    Next state: default state.
    """
    await message.answer(text=cancel_text)
    await state.clear()


@router.message(Command(commands='mistake'), StateFilter(default_state))
async def process_mistake_command(message: Message, state: FSMContext):
    """
    Handler responding to the mistake command.
    Prompts to enter a username in the next state.

    Args:
        message: '/mistake' command
        state: default state.

    Next state: fill name state.
    """
    await message.answer(text=enter_name_text)
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    """
    Handler receiving username.
    When receiving a name, the data is checked for validity.
    After adding information to the database, moves to the next state.

    Args:
        message: username.
        state: fill name state.

    Previous state: default state.
    Next state: fill mistake state.
    """
    user_id = message.from_user.id
    name = message.text
    generated_id = await insert_user_name(user_id, name)

    await state.update_data(name=name, id=generated_id)
    await message.answer(text=accepted_name_text)

    await state.set_state(FSMFillForm.fill_mistake)


@router.message(StateFilter(FSMFillForm.fill_mistake), F.text)
async def process_mistake_sent(message: Message, state: FSMContext):
    """
    Handler receiving brief information about violation.
    Prompts to enter a detailed description in the next state.

    Args:
        message: brief information about violation.
        state: fill mistake state.

    Previous state: fill name state.
    Next state: fill description state.
    """

    id_ = await get_user_id(state)
    mistake = message.text

    await insert_mistake(mistake, id_)

    await message.answer(text=accepted_mistake_text)

    await state.set_state(FSMFillForm.fill_description)


@router.message(StateFilter(FSMFillForm.fill_description), F.text)
async def process_description_sent(message: Message, state: FSMContext):
    """
    Handler receiving detailed description of violation.
    Prompts to choose the importance level in the next state.

    Args:
        message: detailed description of violation.
        state: fill description state.

    Previous state: fill mistake state.
    Next state: fill level state.
    """
    low_level_button = InlineKeyboardButton(
        text='Низкий',
        callback_data='low'
    )
    medium_level_button = InlineKeyboardButton(
        text='Средний',
        callback_data='medium'
    )
    high_level_button = InlineKeyboardButton(
        text='Высокий!',
        callback_data='high'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [low_level_button, medium_level_button, high_level_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    id_ = await get_user_id(state)
    description = message.text

    await insert_description(description, id_)

    await message.answer(text=accepted_description_text,
                         reply_markup=markup)

    await state.set_state(FSMFillForm.fill_level)


@router.callback_query(F.data.in_(['low', 'medium', 'high']))
async def process_level_press(callback: CallbackQuery, state: FSMContext):
    """
    Handler receiving importance level of violation.
    User can choose supposed level from the inline buttons.

    Prompts to enter location, premises number where the violation
    was recorded in the next state.

    Args:
        callback: callback with inline keyboard with 3 levels of importance.
        state: fill level state.

    Previous state: fill description state.
    Next state: fill place state.
    """
    id_ = await get_user_id(state)
    level = callback.data

    await insert_level(level, id_)

    await callback.message.delete()

    await callback.message.answer(text=accepted_level_text)
    await state.set_state(FSMFillForm.fill_place)


@router.message(StateFilter(FSMFillForm.fill_place), F.text)
async def process_place_sent(message: Message, state: FSMContext):
    """
    Handler receiving location, premises number where the violation
    was recorded.
    Prompts to upload the violation photo in the next state.

    Args:
        message: location, premises number where the violation was recorded
        state: fill place state.

    Previous state: fill level state.
    Next state: upload photo state.
    """
    id_ = await get_user_id(state)
    place = message.text

    await insert_place(place, id_)

    await message.answer(text=accepted_place_text)
    await state.set_state(FSMFillForm.upload_photo)


@router.message(StateFilter(FSMFillForm.upload_photo),
                F.photo[-1].as_('latest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             latest_photo: PhotoSize):
    """
    Handler receiving upload the violation photo.
    It adds ing information to the database,
    and informs the user about the successful completion of the request.

    Args:
        message: violation photo.
        state: upload photo state.
        latest_photo: violation photo.

    Previous state: fill place state.
    Next state: None.
    """
    file_id = latest_photo.file_id
    file = await message.bot.get_file(file_id)

    id_ = await get_user_id(state)

    photo_url = (f"https://api.telegram.org/file/bot"
                 f"{message.bot.token}/{file.file_path}")

    await insert_photo(photo_url, id_)

    await state.clear()
    await message.answer(text=accepted_request_text(id_))

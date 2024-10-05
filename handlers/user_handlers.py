import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage #NOT USING
from aiogram.types import (CallbackQuery,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           Message,
                           PhotoSize)

router = Router()

load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')

storage = MemoryStorage() #NEED TO REPLACE

bot = Bot(BOT_TOKEN)
#dp = Dispatcher(storage=storage)

user_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMFillForm(StatesGroup):

    fill_name = State()
    fill_mistake = State()
    fill_description = State()
    fill_level = State()
    fill_place = State()
    fill_date = State()
    upload_photo = State()
    #So, need to add  yagpt question may be and help


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Этот бот принимает заявки выявленных нарушений'
            'требований охраны труда, промышленной и пожарной безопасности\n'
            'Чтобы заявить о нарушении - отправьте команду - /mistake\n'
            'Чтобы задать вопрос нейросети в области охраны труда - '
            'отправьте команду - /bot\n'
            'Чтобы вызвать справку - отправьте команду - /help'
    )

@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(
        text='Программа «Near-miss» — это система учета и анализа инцидентов, которые могли бы привести к несчастным случаям, но были предотвращены в последний момент.\n'
             'Основной целью программы является предотвращение будущих инцидентов путем идентификации и устранения потенциальных опасностей.\n'
             'Несчастные случаи на производстве могут привести к тяжелым травмам, потере рабочей силы и, в крайнем случае, к смерти.\n'
             'Кроме того, они могут привести к существенным финансовым потерям для компании в виде штрафов, компенсаций и потери репутации.'
    )

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего.\n'
             'Чтобы начать пользоваться ботом - '
             'отправьте команду - /mistake'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из формы заполнения заявки нарушений.\n'
            'Чтобы снова перейти к заполнению заявки -'
            'отправьте команду /mistake'
    )
    await  state.clear()

@router.message(Command(commands='mistake'), StateFilter(default_state))
async def process_mistake_command(message: Message, state: FSMContext):
    await message.answer(text=' Пожалуйста, введите ваше имя')
    await state.set_state(FSMFillForm.fill_name)

@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message:Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Благодарю!\n\n'
                              'Теперь укажите краткую информацию о нарушении')
    await state.set_state(FSMFillForm.fill_mistake)

@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )

@router.message(StateFilter(FSMFillForm.fill_mistake))
async def process_mistake_sent(message: Message, state: FSMContext):
    await state.update_data(mistake=message.text)
    await message.answer(text='Благодарю!\n\n'
                              'Теперь укажите подробную информацию о нарушении')
    await state.set_state(FSMFillForm.fill_description)

#NEED TO ADD HANDLER, CATCHING MISTAKE WITH MISTAKE ERROR

@router.message(StateFilter(FSMFillForm.fill_description))
async def process_description_sent(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
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
    await message.answer(text='Благодарю!\n\n'
                              'Теперь укажите предполагаемый уровень опасности',
                         reply_markup=markup)
    await state.set_state(FSMFillForm.fill_level)


@router.callback_query(F.data.in_(['low', 'medium', 'high']))
#message(StateFilter(FSMFillForm.fill_level),
#            F.data.in_(['low', 'medium', 'high']))
async def process_level_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(level=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text='Благодарю! Укажите помещение/место нарушения'
    )
    await state.set_state(FSMFillForm.fill_place)

@router.message(StateFilter(FSMFillForm.fill_level))
async def warning_not_level(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе уровня опасности\n\n'
             'Если вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )

@router.message(StateFilter(FSMFillForm.fill_place))
async def process_place_sent(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await message.answer(text='Благодарю!\n\n'
                              'Теперь загрузите фотографию нарушения')
    await state.set_state(FSMFillForm.upload_photo)

@router.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('latest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             latest_photo: PhotoSize):
    user_id = message.from_user.id

    await state.update_data(
        photo_unique_id=latest_photo.file_unique_id,
        photo_id=latest_photo.file_id
    )

    user_dict[user_id] = await state.get_data()
    #user_dict[latest_photo.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer(
        text='Благодарю! Ваша заявка зарегистрирована.\n'
        'Сотрудники Отдела охраны труда обработают его в '
        'установленные сроки и сообщат о результатах рассмотрения'
    )

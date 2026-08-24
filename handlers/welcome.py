from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.welcome import get_welcome_keyboard

from db.methods.classes import get_classes

from handlers.classes import ClassesFSM

from utils import join

router = Router()

welcome_image = FSInputFile('assets/welcome.png')

def get_welcome_message(message):
    return html.bold(join([
        f'Привіт, {message.from_user.full_name}!',
        '',
        'Я бот, який записує все твоє домашнє завдання 🕰',
        'Обери дію нижче 👇'
    ]))

@router.message(CommandStart())
@router.message(F.text == "🔙 Головне меню")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    classes = get_classes(message.from_user.id)
    await state.clear()
    await state.set_state(ClassesFSM.allclases)

    await message.answer_photo(photo=welcome_image, caption=get_welcome_message(message), reply_markup=get_welcome_keyboard(classes))

@router.callback_query(F.data == "main_menu")
async def main_menu(callback_query: CallbackQuery, state: FSMContext):
    classes = get_classes(callback_query.from_user.id)
    await state.clear()
    await state.set_state(ClassesFSM.allclases)

    await callback_query.message.answer_photo(photo=welcome_image, caption=get_welcome_message(callback_query.message), reply_markup=get_welcome_keyboard(classes))
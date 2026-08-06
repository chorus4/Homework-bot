from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from keyboards.welcome import get_welcome_keyboard

from utils import join

router = Router()

welcome_image = FSInputFile('assets/welcome.png')

def get_welcome_message(message):
    return html.bold(join([
        f'Привіт, {message.from_user.full_name}!',
        '',
        'Я бот, який записує все твоє домашнє завдання 🕰',
        'Вибери дію нижче 👇'
    ]))

@router.message(CommandStart())
@router.message(F.text == "🔙 Головне меню")
async def command_start_handler(message: Message) -> None:
    await message.answer_photo(photo=welcome_image, caption=get_welcome_message(message), reply_markup=get_welcome_keyboard())

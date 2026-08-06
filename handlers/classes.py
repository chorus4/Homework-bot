from aiogram import Router, html, F
from aiogram.types import Message, FSInputFile

from keyboards.classes import get_classes_keyboard

from utils import join

router = Router()

@router.message(F.text == "Мої класси")
async def get_classes(message: Message):
  await message.answer("Осьо твои класи", reply_markup=get_classes_keyboard())
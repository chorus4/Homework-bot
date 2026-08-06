from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_classes_keyboard():
  builder = ReplyKeyboardBuilder()

  builder.row(KeyboardButton(text="Створити новий класс ➕"))



  builder.row(KeyboardButton(text="🔙 Головне меню"))

  return ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
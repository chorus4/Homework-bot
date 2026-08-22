from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_welcome_keyboard(classes):
  builder = ReplyKeyboardBuilder()
  
  builder.add(KeyboardButton(text="Створити новий класс ➕"))
  builder.add(KeyboardButton(text="Дз на завтра"))

  for cl in classes:
    builder.row(KeyboardButton(text=f"{cl.name}"))

  return ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True, one_time_keyboard=True)
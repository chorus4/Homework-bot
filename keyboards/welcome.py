from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_welcome_keyboard():
  return ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мої класси"), KeyboardButton(text="Дз на завтра")],
  ], resize_keyboard=True)
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_lessons_keyboard(lessons):
  builder = InlineKeyboardBuilder()

  for lesson in lessons:
    builder.row(InlineKeyboardButton(text=lesson.name, callback_data="Data"))

  builder.row(InlineKeyboardButton(text="➕ Новий предмет", callback_data="new_lesson"))
  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="class"))

  return builder.as_markup()
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from db.models.lesson import Lesson

class LessonCallback(CallbackData, prefix="lesson"):
    id: int

class DeleteLessonCallback(CallbackData, prefix="delete_lesson"):
    id: int

def get_lessons_keyboard(lessons: list[Lesson]):
  builder = InlineKeyboardBuilder()

  for lesson in lessons:
    builder.row(InlineKeyboardButton(text=lesson.name, callback_data=LessonCallback(id=lesson.id).pack()))

  builder.row(InlineKeyboardButton(text="➕ Новий предмет", callback_data="new_lesson"))
  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="class"))

  return builder.as_markup()

def get_back_command():
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="lessons")]
  ])

def get_delete_keyboard(id):
   return InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="🔙 Назад", callback_data="lessons"), InlineKeyboardButton(text="Так ❌", callback_data=DeleteLessonCallback(id=id).pack())]
   ])
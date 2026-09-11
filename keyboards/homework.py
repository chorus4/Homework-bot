from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from datetime import timedelta
import calendar

class HomeworkCallback(CallbackData, prefix="homework"):
  day: str

class NewHomeworkLessonCallback(CallbackData, prefix="new-homework-lesson"):
  id: int

class NewHomeworkDateCallback(CallbackData, prefix="new-homework-date"):
  date: str

def get_homework_keyboard(day):
  builder = InlineKeyboardBuilder()

  # builder.row(InlineKeyboardButton(text="👈 Попередній день", callback_data=HomeworkCallback(day=(day - timedelta(days=1)).isoformat()).pack()))
  # builder.add(InlineKeyboardButton(text="Наступний день 👉", callback_data=HomeworkCallback(day=(day + timedelta(days=1)).isoformat()).pack()))

  prevday = day - timedelta(days=1)
  nextday = day + timedelta(days=1)

  builder.row(InlineKeyboardButton(text=f"⬅️ {prevday.strftime("%d.%m")}", callback_data=HomeworkCallback(day=prevday.isoformat()).pack()))
  builder.add(InlineKeyboardButton(text=f"● {day.strftime("%d.%m")} ●", callback_data="none"))
  builder.add(InlineKeyboardButton(text=f"{nextday.strftime("%d.%m")} ➡️", callback_data=HomeworkCallback(day=nextday.isoformat()).pack()))

  builder.row(InlineKeyboardButton(text="Нове дз ➕", callback_data="new-homework"))
  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="class"))

  return builder.as_markup()

def get_new_homework_keyboard(lessons, day):
  builder = InlineKeyboardBuilder()

  for lesson in lessons:
      builder.row(InlineKeyboardButton(text=lesson.name, callback_data=NewHomeworkLessonCallback(id=lesson.id).pack()))

  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=HomeworkCallback(day=day.isoformat()).pack()))

  return builder.as_markup()

def get_new_homework_lesson_keyboard(day, dates):
  builder = InlineKeyboardBuilder()

  for date in dates:
    builder.row(InlineKeyboardButton(text=f"{date.strftime("%d.%m")} | {calendar.day_name[date.weekday()]}", callback_data=NewHomeworkDateCallback(date=date.isoformat()).pack()))

  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="new-homework"))
  builder.row(InlineKeyboardButton(text="❌ Відміна", callback_data=HomeworkCallback(day=day.isoformat()).pack()))

  return builder.as_markup()

def get_new_cancel_homework():
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="new-homework")]
  ])

def get_edit_homework_keyboard(day):
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Видалити", callback_data="delete-homework")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data=HomeworkCallback(day=day.isoformat()).pack())],
  ])
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from db.models.schedule import SCEntry
from db.models.lesson import Lesson
from db.methods.lesson import get_lesson

class EntryCallback(CallbackData, prefix="entry"):
  position: int

class ChangeEntryCallback(CallbackData, prefix="change-entry"):
  lesson: int

class ScheduleCallback(CallbackData, prefix="schedule"):
  day: int

def get_schedule_keyboard(entries: list[SCEntry], weekday):
  builder = InlineKeyboardBuilder()

  for i in range(1, 9):
    text = f"{i} | Пусто"
    for entry in entries:
      if entry.position == i:
        lesson = get_lesson(entry.lesson_id)
        text = f"{i} | {lesson.name}"
        
    builder.row(InlineKeyboardButton(text=text, callback_data=EntryCallback(position=i).pack()))

  builder.row(InlineKeyboardButton(text="👈 Попередній день", callback_data=ScheduleCallback(day=weekday - 1 if weekday != 0 else 6).pack()))
  builder.add(InlineKeyboardButton(text="Наступний день 👉", callback_data=ScheduleCallback(day=weekday + 1 if weekday != 6 else 0).pack()))

  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="class"))

  return builder.as_markup()

def get_entry_keyboard(lessons: list[Lesson], day):
  builder = InlineKeyboardBuilder()

  for lesson in lessons:
    builder.row(InlineKeyboardButton(text=lesson.name, callback_data=ChangeEntryCallback(lesson=lesson.id).pack()))

  builder.row(InlineKeyboardButton(text="Пусто ❌", callback_data="delete-entry"))

  builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=ScheduleCallback(day=day).pack()))

  return builder.as_markup()
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from datetime import date

from keyboards.schedule import ScheduleCallback
from keyboards.homework import HomeworkCallback

def get_classes_keyboard(classes):
  builder = ReplyKeyboardBuilder()

  builder.row(KeyboardButton(text="Створити новий класс ➕"))

  for cl in classes:
    builder.row(KeyboardButton(text=f"{cl.name}"))

  builder.row(KeyboardButton(text="🔙 Головне меню"))

  return ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)

def get_new_class_keyboard():
  return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔙 Головне меню")]], resize_keyboard=True)

def get_class_keyboard(day: date):
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Розклад", callback_data=ScheduleCallback(day=day.weekday()).pack()), InlineKeyboardButton(text="Предмети", callback_data="lessons")],
    [InlineKeyboardButton(text="ДЗ", callback_data=HomeworkCallback(day=day.isoformat()).pack())],
    [InlineKeyboardButton(text="🔙 Головне меню", callback_data="main_menu")]
  ])
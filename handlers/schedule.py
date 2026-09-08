from aiogram import Router, F, html
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import calendar
import logging

from keyboards.schedule import get_schedule_keyboard, get_entry_keyboard, EntryCallback, ChangeEntryCallback, ScheduleCallback

from db.methods.schedule import get_entries_by_day, change_entry, delete_entry
from db.methods.lesson import get_lessons

from utils import join

router = Router()

def get_schedule_message(day_name):
  return html.bold(join([
    f"Розклад на {day_name}"
  ]))

def get_entry_message():
  return html.bold(join([
    "Зміна розкладу"
  ]))

@router.callback_query(ScheduleCallback.filter())
async def schedule_handler(callback_query: CallbackQuery, callback_data: ScheduleCallback, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  weekday = callback_data.day
  
  entries = get_entries_by_day(weekday, class_id)

  await state.update_data(weekday=weekday)

  await callback_query.message.edit_text(get_schedule_message(calendar.day_name[weekday]), reply_markup=get_schedule_keyboard(entries, weekday))

@router.callback_query(EntryCallback.filter())
async def entry_handler(callback_query: CallbackQuery, callback_data: EntryCallback, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  weekday = state_data["weekday"]
  lessons = get_lessons(class_id)

  logging.info(weekday)

  await state.update_data(position=callback_data.position)

  await callback_query.message.edit_text(get_entry_message(), reply_markup=get_entry_keyboard(lessons, weekday))

@router.callback_query(ChangeEntryCallback.filter())
async def change_entry_handler(callback_query: CallbackQuery, callback_data: ChangeEntryCallback, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  lessons = get_lessons(class_id)

  weekday = state_data["weekday"]
  position = state_data["position"]
  logging.info(weekday)

  change_entry(class_id, weekday, position, callback_data.lesson)

  entries = get_entries_by_day(weekday, class_id)

  await callback_query.answer("Успішно")
  await callback_query.message.edit_text(get_schedule_message(calendar.day_name[weekday]), reply_markup=get_schedule_keyboard(entries, weekday))

@router.callback_query(F.data == "delete-entry")
async def delete_entry_handler(callback_query: CallbackQuery, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]

  weekday = state_data["weekday"]
  position = state_data["position"]

  delete_entry(class_id, weekday, position)

  entries = get_entries_by_day(weekday, class_id)

  await callback_query.answer("Успішно")
  await callback_query.message.edit_text(get_schedule_message(calendar.day_name[weekday]), reply_markup=get_schedule_keyboard(entries, weekday))
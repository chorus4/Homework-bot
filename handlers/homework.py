from aiogram import Router, F, html
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from datetime import date, timedelta
import calendar
import logging

from keyboards.homework import HomeworkCallback, NewHomeworkLessonCallback, NewHomeworkDateCallback, get_homework_keyboard, get_new_homework_keyboard, get_new_homework_lesson_keyboard, get_new_cancel_homework

from db.methods.lesson import get_lessons, get_lesson
from db.methods.schedule import get_entries_by_lesson_dif_day
from db.methods.homework import create_homework, get_homeworks

from utils import join

router = Router()

class HomeworkFSM(StatesGroup):
  text = State()

def get_homework_message(day_name, class_id):
  homeworks = get_homeworks(class_id)
  text = [
    f"Дз на {day_name}",
    ""
  ]
  for homework in homeworks:
    text.append(f"{homework.date.strftime("%d.%m")} | {get_lesson(homework.lesson_id).name} | {homework.content}")

  return html.bold(join(text))

def get_new_homework_message():
  return html.bold(join([
    f"Обери предмет 👇"
  ]))

def get_new_homework_lesson_message():
  return html.bold(join([
    f"Обери урок 👇"
  ]))

def get_new_homework_date_message():
  return html.bold(join([
    f"Введи дз 👇"
  ]))

@router.callback_query(HomeworkCallback.filter())
async def homework_handler(callback_query: CallbackQuery, callback_data: HomeworkCallback, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  day = date.fromisoformat(callback_data.day)
  await state.update_data(day=day.isoformat())

  await callback_query.message.edit_text(get_homework_message(f"{day.strftime("%d %B")} ({calendar.day_name[day.weekday()]})", class_id), reply_markup=get_homework_keyboard(day))

@router.callback_query(F.data == "new-homework")
async def new_homework_callback(callback_query: CallbackQuery, state: FSMContext):
  await state.set_state(None)
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  day = date.fromisoformat(state_data["day"])
  lessons = get_lessons(class_id)

  await callback_query.message.edit_text(get_new_homework_message(), reply_markup=get_new_homework_keyboard(lessons, day))

@router.callback_query(NewHomeworkLessonCallback.filter())
async def new_homework_lesson_callback(callback_query: CallbackQuery, callback_data: NewHomeworkLessonCallback, state: FSMContext):
  state_data = await state.get_data()
  lesson_id = callback_data.id
  class_id = state_data["class_id"]
  day = date.fromisoformat(state_data["day"])

  entries = get_entries_by_lesson_dif_day(class_id, lesson_id)
  entries = sorted(entries, key=lambda x: (x.day_num - day.weekday()) % 7)
  dates = []
  for item in entries:
        offset = (item.day_num - day.weekday()) % 7
        dates.append(day + timedelta(days=offset))

  logging.info(dates)

  await state.update_data(lesson=lesson_id)
  await callback_query.message.edit_text(get_new_homework_lesson_message(), reply_markup=get_new_homework_lesson_keyboard(day, dates))

@router.callback_query(NewHomeworkDateCallback.filter())
async def new_homework_date_callback(callback_query: CallbackQuery, callback_data: NewHomeworkDateCallback, state: FSMContext):
  await state.update_data(day=callback_data.date)
  await state.set_state(HomeworkFSM.text)
  
  await callback_query.message.edit_text(get_new_homework_date_message(), reply_markup=get_new_cancel_homework())

@router.message(HomeworkFSM.text)
async def new_homework_text_handler(message: Message, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  lesson_id = state_data["lesson"]
  day = date.fromisoformat(state_data["day"])
  text = message.text

  create_homework(class_id, lesson_id, day, text)

  await message.answer(get_homework_message(f"{day.strftime("%d %B")} ({calendar.day_name[day.weekday()]})", class_id), reply_markup=get_homework_keyboard(day))
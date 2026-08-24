from aiogram import Router, F, html
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.lessons import get_lessons_keyboard, get_back_command, get_delete_keyboard, LessonCallback, DeleteLessonCallback

from db.methods.classes import get_class
from db.methods.lesson import get_lessons, create_lesson, get_lesson, delete_lesson

from utils import join

import logging

router = Router()

class LessonFSM(StatesGroup):
  new_lesson = State()

def get_lessons_message(class_name):
  return html.bold(join([
    f"Предмети класа: {class_name}"
  ]))

@router.callback_query(F.data == "lessons")
async def lessons_handler(callback_query: CallbackQuery, state: FSMContext):
  await state.set_state(None)
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  class_ = get_class(class_id)
  lessons = get_lessons(class_.id)

  await callback_query.message.edit_text(get_lessons_message(class_.name), reply_markup=get_lessons_keyboard(lessons))

@router.callback_query(F.data == "new_lesson")
async def new_lesson_handler(callback_query: CallbackQuery, state: FSMContext):
  await state.set_state(LessonFSM.new_lesson)
  await callback_query.message.edit_text(html.bold("Введіть назву предмета"), reply_markup=get_back_command())

@router.message(LessonFSM.new_lesson)
async def new_lesson_name_handler(message: Message, state: FSMContext):
  logging.debug("New lesson")

  state_data = await state.get_data()
  await state.set_state(None)
  class_id = state_data["class_id"]
  class_ = get_class(class_id)
  create_lesson(class_.id, message.text)
  lessons = get_lessons(class_.id)

  await message.answer(get_lessons_message(class_.name), reply_markup=get_lessons_keyboard(lessons))

@router.callback_query(LessonCallback.filter())
async def lesson_callback(callback_query: CallbackQuery, callback_data: LessonCallback):
  lesson = get_lesson(callback_data.id)

  await callback_query.message.edit_text(html.bold(f"Ви впевнені що хочете видалити предмет: {lesson.name}?"), reply_markup=get_delete_keyboard(lesson.id))

@router.callback_query(DeleteLessonCallback.filter())
async def delete_lesson_callback(callback_query: CallbackQuery, callback_data: DeleteLessonCallback, state: FSMContext):
  lesson_id = callback_data.id

  delete_lesson(lesson_id)

  await callback_query.answer("Успішно")
  await lessons_handler(callback_query, state)
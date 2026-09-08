from aiogram import Router, html, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.deep_linking import create_start_link

from keyboards.classes import get_classes_keyboard, get_new_class_keyboard, get_class_keyboard

from db.methods.classes import create_class, get_class
from db.models.classes import Class

from utils import join, get_todays_day

import logging

router = Router()

class ClassesFSM(StatesGroup):
  allclases = State()
  newclass = State()
  class_id = State()

def get_class_message(class_: Class, link):
  return html.bold(join([
    f"Клас: {class_.name}",
    f"",
    f"Посилання: {link}",
    f"Обери дію нижче 👇"
  ]))

@router.message(F.text == "Створити новий класс ➕")
async def create_class_handler(message: Message, state: FSMContext):
  await state.set_state(ClassesFSM.newclass)
  await message.answer(html.bold("Введи ім'я нового классу"), reply_markup=get_new_class_keyboard())

@router.message(ClassesFSM.newclass)
async def name_class_handler(message: Message, state: FSMContext):
  create_class(message.from_user.id, message.text)
  await state.clear()
  await state.set_state(ClassesFSM.allclases)
  await message.answer(html.bold("Успішно"))
  await message.answer(html.bold("Обери дію нижче 👇"), reply_markup=get_classes_keyboard())

@router.message(ClassesFSM.allclases)
async def class_handler(message: Message, state: FSMContext):
  logging.info("Handled class")
  class_ = get_class(message.text)
  if class_ == None: return

  await state.update_data(class_id = class_.id)
  await message.answer(get_class_message(class_, await create_start_link(message.bot, class_.link)), reply_markup=get_class_keyboard(get_todays_day()))

@router.callback_query(F.data == "class")
async def get_class_handler(callback_query: CallbackQuery, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  class_ = get_class(class_id)

  await state.update_data(class_id = class_.id)
  await callback_query.message.edit_text(get_class_message(class_, await create_start_link(callback_query.bot, class_.link)), reply_markup=get_class_keyboard(get_todays_day()))
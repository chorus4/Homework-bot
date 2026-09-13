from aiogram import Router, html, F
from aiogram.types import Message, CallbackQuery, MessageReactionUpdated
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.deep_linking import create_start_link
from aiogram.filters import CommandStart, CommandObject, StateFilter, MagicData

from keyboards.classes import get_new_class_keyboard, get_class_keyboard, get_delete_class_keyboard
from keyboards.welcome import get_welcome_keyboard

from db.methods.classes import create_class, get_class, get_classes, delete_class, get_class_by_link
from db.methods.access import get_access_by_all, delete_access, create_access, check_access
from db.models.classes import Class

from utils import join, get_todays_day

import logging
import uuid

router = Router()

class ClassesFSM(StatesGroup):
  allclases = State()
  newclass = State()
  class_id = State()
  delete_class = State()

def get_class_message(class_: Class, link):
  return html.bold(join([
    f"Клас: {class_.name}",
    f"",
    f"Посилання: {link}",
    f"Обери дію нижче 👇"
  ]))

def get_welcome_message(full_name):
    return html.bold(join([
        f'Привіт, {full_name}!',
        '',
        'Я бот, який записує все твоє домашнє завдання 🕰',
        'Обери дію нижче 👇'
    ]))

def get_delete_class_message():
    return html.bold(join([
        'Ти впевнений?',
        'Для підтвердження постав реакцію на повідомлення'
    ]))

@router.message(F.text == "Створити новий класс ➕")
async def create_class_handler(message: Message, state: FSMContext):
  await state.set_state(ClassesFSM.newclass)
  await message.answer(html.bold("Введи ім'я нового классу"), reply_markup=get_new_class_keyboard())

# Add access
@router.message(CommandStart(deep_link=True), StateFilter("*"), MagicData(~F.command.args.startswith('h')))
async def add_access_handler(message: Message, command: CommandObject, state: FSMContext):
  access_link = command.args
  class_ = get_class_by_link(uuid.UUID(access_link))

  if check_access(message.from_user.id, class_.id):
    await message.delete()
    return

  create_access(class_.id, message.from_user.id, 'invited')
  await state.update_data(class_id = class_.id)
  await message.answer(get_class_message(class_, await create_start_link(message.bot, class_.link)), reply_markup=get_class_keyboard(get_todays_day()))

@router.message(ClassesFSM.newclass)
async def name_class_handler(message: Message, state: FSMContext):
  create_class(message.from_user.id, message.text)
  classes = get_classes(message.from_user.id)
  await state.clear()
  await state.set_state(ClassesFSM.allclases)
  await message.answer(html.bold("Успішно"))
  await message.answer(get_welcome_message(message.from_user.full_name), reply_markup=get_welcome_keyboard(classes))

@router.message(ClassesFSM.allclases)
async def class_handler(message: Message, state: FSMContext):
  logging.info("Handled class")
  class_ = get_class(message.text)
  if class_ == None: return
  await state.set_state(None)

  await state.update_data(class_id = class_.id)
  await message.answer(get_class_message(class_, await create_start_link(message.bot, class_.link)), reply_markup=get_class_keyboard(get_todays_day()))

@router.callback_query(F.data == "class")
async def get_class_handler(callback_query: CallbackQuery, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  class_ = get_class(class_id)

  await state.set_state(None)
  await state.update_data(class_id = class_.id)
  await callback_query.message.edit_text(get_class_message(class_, await create_start_link(callback_query.bot, class_.link)), reply_markup=get_class_keyboard(get_todays_day()))

# Delete class

@router.callback_query(F.data == "delete-class")
async def delete_lesson_handler(callback_query: CallbackQuery, state: FSMContext):

  await state.set_state(ClassesFSM.delete_class)
  await callback_query.message.edit_text(get_delete_class_message(), reply_markup=get_delete_class_keyboard())

@router.message_reaction(ClassesFSM.delete_class)
async def message_reaction_handler(reaction: MessageReactionUpdated, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  access = get_access_by_all(class_id, reaction.user.id)

  if access.role == 'owner':
    delete_class(class_id)
  elif access.role == 'invited':
    delete_access(access.id)

  classes = get_classes(reaction.user.id)
  await state.set_state(ClassesFSM.allclases)
  await reaction.bot.delete_message(chat_id=reaction.user.id, message_id=reaction.message_id)
  await reaction.bot.send_message(text=get_welcome_message(reaction.user.full_name), reply_markup=get_welcome_keyboard(classes), chat_id=reaction.user.id)
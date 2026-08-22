from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.lessons import get_lessons_keyboard

from db.methods.classes import get_class

from utils import join

router = Router()

def get_lessons_message():
  return html.bold(join([
    f"Lessons"
  ]))

@router.callback_query(F.data == "lessons")
async def lessons_handler(callback_query: CallbackQuery, state: FSMContext):
  state_data = await state.get_data()
  class_id = state_data["class_id"]
  class_ = get_class(class_id)

  await callback_query.message.edit_text(get_lessons_message(), reply_markup=get_lessons_keyboard([]))
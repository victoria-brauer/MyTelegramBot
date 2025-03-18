from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from keyboards_box.talk_kb import get_personality_keyboard, get_end_keyboard
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()


PERSONALITIES = {
    "einstein": "Ты Альберт Эйнштейн. Объясняй всё с научной точки зрения.",
    "shakespeare": "Ты Уильям Шекспир. Отвечай в стиле поэтического английского.",
    "julius": "Ты конь Юлий. Mультяшный персонаж российской франшизы мультфильмов «Три богатыря». Отвечай в шуточной форме.",
    "pamela": "Ты Памела Андерсон. Заигрывай и флиртуй."
}


@router.message(Command("talk"))
async def talk_command(message: types.Message):
    await message.answer("Выберите личность с которой хотите поговорить:", reply_markup=get_personality_keyboard())

@router.callback_query(lambda c: c.data in PERSONALITIES)
async def select_personality(callback: CallbackQuery):
    personality = callback.data
    gpt_service.set_system_message(PERSONALITIES[personality])
    await callback.message.edit_text(f"Вы выбрали {personality.capitalize()}! Теперь можете задать вопросы.", reply_markup=get_end_keyboard())

@router.message()
async def handle_message(message: types.Message):
    response = gpt_service.get_response(message.text)
    await message.answer(response, reply_markup=get_end_keyboard())

@router.callback_query(lambda c: c.data == "end")
async def end_chat(callback: CallbackQuery):
    await callback.message.edit_text("Чат завершен. Введите /talk, чтобы начать снова.")
from aiogram import Router, types
from aiogram.filters.command import Command
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service = ChatGPTService()

gpt_service.set_system_message("Ты большая энциклопедия. Отвечай короткими, но интересными фактами")


@router.message(Command("gpt"))
async def command_gpt(message: types.Message):
    await message.answer(f"Привет, {message.chat.first_name}! Введи свою тему для интересного факта! \U0001F60E")


@router.message()
async def handle_message(message: types.Message):
    gpt_service.add_user_message(message.text)

    response = gpt_service.get_response()
    await message.answer(response)
from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards_box.keyboards import kb1


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.chat.first_name}! Выберите действие!\U0001F338", reply_markup=kb1)


@router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer(f"До новых встреч, {message.chat.first_name}!Спасибо за использование бота! Введи /start, если хочешь начать снова.\U0001F338", reply_markup=kb1)
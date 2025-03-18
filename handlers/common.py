from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards_box.keyboards import kb1

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.chat.first_name}! Выбери действие!", reply_markup=kb1)



# @router.message(F.text & ~F.text.startswith("/gpt"))  # Исключаем "/gpt"
# async def echo(message: types.Message):
#     print(message.text)
#     if "stop" in message.text:
#         await message.answer("Спасибо за использование бота! Введите /start, если хотите начать снова.")
#     else:
#         await message.answer(message.text)
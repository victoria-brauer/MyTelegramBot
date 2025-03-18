from aiogram import Router, types
from aiogram.filters.command import Command
from utils.random_image import space


router = Router()


@router.message(Command("space"))
@router.message(Command("космос"))
async def command_space(message: types.Message):
    title, url = space()
    await message.answer(f"Лови космическое фото дня\U0001F680: {title}\U0001F52D")
    await message.answer_photo(url)



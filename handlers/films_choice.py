from aiogram import Router, types
from aiogram.filters.command import Command
from keyboards_box.kb_recommend import get_main_menu, get_choice_buttons
from utils.gpt_service import ChatGPTService

router = Router()
chat_gpt = ChatGPTService()

user_disliked = {}

@router.message(Command("recommend"))
async def command_gpt(message: types.Message):
    await message.answer(
        f"Привет, {message.chat.first_name}! Я бот, который помогает выбрать лучшее в мире книг, фильмов и музыки.\U0001F4D6 "
        "Выберите категорию:",
        reply_markup=get_main_menu()
    )

@router.callback_query(lambda c: c.data.startswith("category_"))
async def choose_category(callback: types.CallbackQuery):
    category = callback.data.split("_")[1]

    genres = {
        "films": ["Драма", "Комедия", "Фантастика", "Ужасы", "Триллер"],
        "books": ["Фэнтези", "Детектив", "Роман", "История", "Научная фантастика"],
        "music": ["Рок", "Поп", "Джаз", "Техно", "Классическая"]
    }

    buttons = [[types.InlineKeyboardButton(text=genre, callback_data=f"genre_{category}_{genre}")] for genre in genres[category]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(f"Выберите жанр {category}:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("genre_"))
async def choose_genre(callback: types.CallbackQuery):
    _, category, genre = callback.data.split("_")

    user_id = callback.from_user.id
    if user_id not in user_disliked:
        user_disliked[user_id] = []

    recommendation = chat_gpt.get_recommendation(category, genre, user_disliked[user_id])

    await callback.message.edit_text(f"Я рекомендую вам:\n\n{recommendation}", reply_markup=get_choice_buttons())

@router.callback_query(lambda c: c.data == "dislike")
async def dislike_recommendation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    last_recommendation = callback.message.text.split("\n\n")[1]

    user_disliked[user_id].append(last_recommendation)

    await callback.answer("Запомнил, ищу другой вариант...")

    await choose_genre(callback)

@router.callback_query(lambda c: c.data == "end")
async def end_recommendation(callback: types.CallbackQuery):
    await callback.message.edit_text("Спасибо за использование бота! Введите /recommend, если хотите начать снова.")


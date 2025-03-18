from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="Фильмы", callback_data="category_films")],
        [InlineKeyboardButton(text="Книги", callback_data="category_books")],
        [InlineKeyboardButton(text="Музыка", callback_data="category_music")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_choice_buttons():
    buttons = [
        [InlineKeyboardButton(text="Не нравится", callback_data="dislike")],
        [InlineKeyboardButton(text="Закончить", callback_data="end")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
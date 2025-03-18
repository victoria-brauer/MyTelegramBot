from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_column_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=button)] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
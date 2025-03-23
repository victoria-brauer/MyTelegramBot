from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_topic_keyboard():
    buttons = [
        [InlineKeyboardButton(text="История", callback_data="quiz_history")],
        [InlineKeyboardButton(text="Наука", callback_data="quiz_science")],
        [InlineKeyboardButton(text="География", callback_data="quiz_geography")],
        [InlineKeyboardButton(text="Литература", callback_data="quiz_literature")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_quiz_buttons():
    buttons = [
        [InlineKeyboardButton(text="🎭 Сменить тему", callback_data="change_topic")],
        [InlineKeyboardButton(text="🏁 Закончить квиз", callback_data="end_quiz")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

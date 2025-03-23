from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_personality_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Альберт Эйнштейн", callback_data="einstein")],
        [InlineKeyboardButton(text="Уильям Шекспир", callback_data="shakespeare")],
        [InlineKeyboardButton(text="Конь Юлий", callback_data="julius")],
        [InlineKeyboardButton(text="Памела Андерсон", callback_data="pamela")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

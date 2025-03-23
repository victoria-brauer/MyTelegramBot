from aiogram import types

button_1 = types.KeyboardButton(text="/start")
button_2 = types.KeyboardButton(text="/space")
button_3 = types.KeyboardButton(text="/recommend")
button_4 = types.KeyboardButton(text="/resume")
button_5 = types.KeyboardButton(text="/gpt")
button_6 = types.KeyboardButton(text="/talk")
button_7 = types.KeyboardButton(text="/quiz")
button_8 = types.KeyboardButton(text="/stop")

keyboard_1 = [
    [button_1, button_2],
    [button_3, button_4],
    [button_5, button_6],
    [button_7, button_8],
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)
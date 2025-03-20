from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.gpt_service import ChatGPTService

router = Router()

gpt_service_chat = ChatGPTService()

gpt_service_chat.set_system_message("Ты большая энциклопедия. Отвечай короткими, но интересными фактами")


def get_stop_button():
    """Создает кнопку 'Завершить' для остановки взаимодействия."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛑 Завершить", callback_data="stop_gpt")]
        ]
    )


@router.message(Command("gpt"))
async def command_gpt(message: types.Message):
    await message.answer(
        f"Привет, {message.chat.first_name}! Введи свою тему для интересного факта! \U0001F60E",
        reply_markup=get_stop_button()
    )


@router.message()
async def handle_message(message: types.Message):
    gpt_service_chat.add_user_message(message.text)

    response = gpt_service_chat.get_response(message.text)

    await message.answer(response, reply_markup=get_stop_button())


@router.callback_query(lambda c: c.data == "stop_gpt")
async def stop_gpt(callback: types.CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Завершить' и очищает историю сообщений."""
    gpt_service_chat.message_history = []  # Очищаем историю сообщений

    await callback.message.edit_text("🛑 Окей, жду новых запросов! Введи /gpt, чтобы начать заново.")
    await callback.answer()

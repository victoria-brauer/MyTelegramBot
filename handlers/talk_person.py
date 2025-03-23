from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from keyboards_box.talk_kb import get_personality_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.gpt_service import ChatGPTService


router = Router()
gpt_service_talk = ChatGPTService()


PERSONALITIES = {
    "einstein": "Ты Альберт Эйнштейн. Объясняй всё с научной точки зрения.",
    "shakespeare": "Ты Уильям Шекспир. Отвечай в стиле поэтического английского.",
    "julius": "Ты Конь Юлий. Mультяшный персонаж российской франшизы мультфильмов «Три богатыря». Отвечай в шуточной форме.",
    "pamela": "Ты Памела Андерсон. Заигрывай и флиртуй."
}

user_personality = {}


def get_stop_talk():
    """Создает кнопку 'Завершить' для остановки взаимодействия."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛑 Завершить", callback_data="stop_talk")]
        ]
    )


@router.message(Command("talk"))
async def talk_command(message: types.Message):
    """Команда /talk - выбор личности"""
    await message.answer("Выберите личность, с которой хотите поговорить:", reply_markup=get_personality_keyboard())


@router.callback_query(lambda c: c.data in PERSONALITIES)
async def select_personality(callback: CallbackQuery):
    """Выбор персонажа для общения"""
    user_id = callback.from_user.id
    personality = callback.data
    user_personality[user_id] = personality

    # Устанавливаем контекст для GPT
    gpt_service_talk.set_system_message(PERSONALITIES[personality])

    await callback.message.edit_text(f"Вы выбрали {personality.capitalize()}! Теперь можете задать вопросы.",
                                     reply_markup=get_stop_talk())

@router.message(lambda message: message.from_user.id in user_personality)
async def handle_message(message: types.Message):
    """Обрабатывает ответ от выбранного персонажа"""
    user_id = message.from_user.id
    response = gpt_service_talk.get_personality_response(message.text)
    await message.answer(response, reply_markup=get_stop_talk())


@router.callback_query(lambda c: c.data == "stop_talk")
async def stop_talk(callback: types.CallbackQuery):
    """Обрабатывает нажатие на кнопку 'Завершить' и очищает историю сообщений."""
    user_id = callback.from_user.id
    user_personality.pop(user_id, None)
    gpt_service_talk.reset_history()

    await callback.message.edit_text("Чат завершен. Введите /talk, чтобы начать снова.")
    await callback.answer()



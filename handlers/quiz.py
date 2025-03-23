from aiogram import Router, types
from aiogram.filters import Command
from keyboards_box.quiz_kb import get_topic_keyboard, get_quiz_buttons
from utils.gpt_service import ChatGPTService
from difflib import SequenceMatcher


router = Router()
chat_gpt = ChatGPTService()

user_data = {}


def get_user_data(user_id):
    return user_data.setdefault(user_id, {"score": 0, "question_count": 0, "topic": None, "answer": None})


def is_similar(user_answer, correct_answer, threshold=0.5):
    return SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio() >= threshold


@router.message(Command("quiz"))
async def start_quiz(message: types.Message):
    await message.answer("Выбери тему квиза:", reply_markup=get_topic_keyboard())


@router.callback_query(lambda c: c.data.startswith("quiz_"))
async def quiz_topic(callback: types.CallbackQuery):
    user = get_user_data(callback.from_user.id)
    user.update({"score": 0, "question_count": 0, "topic": callback.data.replace("quiz_", "")})
    await callback.message.edit_text(f"Вы выбрали тему: {user['topic']}. Начинаем!")
    await send_quiz_question(callback.message, callback.from_user.id)


async def send_quiz_question(message: types.Message, user_id: int):
    user = get_user_data(user_id)

    if user["question_count"] >= 5:
        return await finish_quiz(message, user_id)

    response = chat_gpt.get_quiz_question(user['topic'])
    if "Ответ:" in response:
        question, answer = response.rsplit("Ответ:", 1)
        user.update({"answer": answer.strip(), "question_count": user["question_count"] + 1})
        await message.answer(f"Вопрос {user['question_count']}/5:\n\n{question.strip()}",
                             reply_markup=get_quiz_buttons())
    else:
        await message.answer("Ошибка генерации вопроса. Попробуйте снова.")


@router.message(lambda message: message.from_user.id in user_data and user_data[message.from_user.id]["answer"])
async def check_answer(message: types.Message):
    user = get_user_data(message.from_user.id)
    correct_answer = user["answer"].lower()

    if is_similar(message.text, correct_answer):
        user["score"] += 1
        reply = "✅ Верно!"
    else:
        reply = f"❌ Неверно. Правильный ответ: {correct_answer}"

    await message.answer(reply, reply_markup=get_quiz_buttons())
    await send_quiz_question(message, message.from_user.id)


async def finish_quiz(message: types.Message, user_id: int):
    user = get_user_data(user_id)

    if user["score"] >= 4:
        result = "🎉 Отлично!"
    elif user["score"] >= 2:
        result = "😊 Средне."
    else:
        result = "😞 Нужно подтянуть знания."

    await message.answer(
        f"{result} Вы правильно ответили на {user['score']} из 5 вопросов.\n\n"
        f"Для нового квиза нажмите /quiz"
    )
    user_data.pop(user_id, None)


@router.callback_query(lambda c: c.data == "new_question")
async def new_question(callback: types.CallbackQuery):
    await callback.message.delete()
    await send_quiz_question(callback.message, callback.from_user.id)
    await callback.answer()


@router.callback_query(lambda c: c.data == "change_topic")
async def change_topic(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите новую тему:", reply_markup=get_topic_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "end_quiz")
async def end_quiz(callback: types.CallbackQuery):
    await finish_quiz(callback.message, callback.from_user.id)
    await callback.answer()




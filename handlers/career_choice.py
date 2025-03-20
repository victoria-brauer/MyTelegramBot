from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards_box.resume_keyboards import make_column_keyboard

router = Router()

choice_education = [
    "Среднее",
    "Профессионально-техническое",
    "Средне специальное",
    "Высшее",
]

choice_experience = [
    "Нет опыта",
    "Менее 1 года",
    "1-3 года",
    "3-5 лет",
    "Более 5 лет",
]

choice_skills = [
    "Коммуникабельность",
    "Лидерство",
    "Работа в команде",
    "Аналитическое мышление",
    "Управление проектами",
    "Продажи",
    "Программирование",
    "Маркетинг",
    "Дизайн",
]


class CareerChoice(StatesGroup):
    education = State()
    experience = State()
    skills = State()


@router.message(Command("resume"))
async def command_resume(message: types.Message, state: FSMContext):
    await message.answer("Ваше образование", reply_markup=make_column_keyboard(choice_education))
    await state.set_state(CareerChoice.education)


@router.message(CareerChoice.education, F.text.in_(choice_education))
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(selected_education=message.text)
    await message.answer("Ваш опыт работы", reply_markup=make_column_keyboard(choice_experience))
    await state.set_state(CareerChoice.experience)


@router.message(CareerChoice.experience, F.text.in_(choice_experience))
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(selected_experience=message.text)
    await message.answer("Ваши навыки", reply_markup=make_column_keyboard(choice_skills))
    await state.set_state(CareerChoice.skills)


@router.message(CareerChoice.education)
async def education_incorrect(message: types.Message):
    await message.answer("Выберите одно из предложенных значений! \U0001F60A", reply_markup=make_column_keyboard(choice_education))


@router.message(CareerChoice.skills, F.text.in_(choice_skills))
async def process_vacancy(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    result_text = (
        f'✅ Анкета заполнена!\n\n'
        f'🎓 Образование: {user_data["selected_education"]}\n'
        f'💼 Опыт работы: {user_data["selected_experience"]}\n'
        f'🛠 Навыки: {message.text}\n\n'
        f'🔄 Чтобы заполнить заново, введите команду /resume\n'
        f'🛑 Чтобы завершить работу или вернуться к выбору действий, введите команду /stop'
    )
    await message.answer(result_text, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router.message(CareerChoice.experience)
async def education_incorrect(message: types.Message):
    await message.answer("Выберите одно из предложенных значений! \U0001F60A", reply_markup=make_column_keyboard(choice_experience))


@router.message(CareerChoice.skills)
async def education_incorrect(message: types.Message):
    await message.answer("Выберите одно из предложенных значений! \U0001F60A", reply_markup=make_column_keyboard(choice_skills))

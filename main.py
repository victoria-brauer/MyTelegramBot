import config
import logging
from aiogram import Bot, Dispatcher
import asyncio
from handlers import common, career_choice, gpt_chat, space_photo, films_choice, talk_person, quiz



async def main():
    TOKEN_API = config.TOKEN_TG

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN_API)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(career_choice.router)
    dp.include_router(films_choice.router)
    dp.include_router(space_photo.router)
    dp.include_router(quiz.router)
    dp.include_router(talk_person.router)
    dp.include_router(gpt_chat.router)



    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())







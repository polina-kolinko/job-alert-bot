import asyncio
from aiogram import Bot, Dispatcher
from aiogram import F
from app.config import BOT_TOKEN
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.trudvsem_api import get_vacancies, format_vacancy

dp = Dispatcher()

@dp.message(CommandStart())
async def answer(message: Message):
    await message.answer("Привет! Я помогу искать новые вакансии.")
@dp.message(F.text)
async def dialog(message: Message):
    query = message.text.strip()
    vacancies = get_vacancies(query)
    if vacancies is None:
        await message.answer("не удалось получить вакансии")
    elif not vacancies:
        await message.answer("По вашему запросу вакансий не найдено")
    else:
        for item in vacancies:
            elem = item['vacancy']
            await message.answer(format_vacancy(elem))


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
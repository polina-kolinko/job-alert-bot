import asyncio
from aiogram import Bot, Dispatcher
from aiogram import F
from app.config import BOT_TOKEN
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from app.trudvsem_api import get_vacancies, format_vacancy
from app.database import init_db, add_subscription, get_subscriptions

dp = Dispatcher()

@dp.message(CommandStart())
async def answer(message: Message):
    await message.answer("Привет! Я помогу искать новые вакансии.")

@dp.message(Command("subscribe"))
async def subscribe(message: Message):
    telegram_user_id = message.from_user.id
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Напиши запрос после команды, например /subscribe python")
    else:
        text = parts[1]
        await add_subscription(telegram_user_id, text)
        await message.answer("Подписка добавлена")

@dp.message(Command("subscriptions"))
async def show_subscriptions(message: Message):
    telegram_user_id = message.from_user.id
    rows = await get_subscriptions(telegram_user_id)
    text = "Ваши подписки:\n"
    if len(rows) == 0:
        await message.answer("Подписки отсутствуют")
    else:
        for elem in rows:
            text += elem[0] + "\n"
        await message.answer(text)


@dp.message(F.text)
async def dialog(message: Message):
    query = message.text.strip()
    vacancies = await get_vacancies(query)
    if vacancies is None:
        await message.answer("не удалось получить вакансии")
    elif not vacancies:
        await message.answer("По вашему запросу вакансий не найдено")
    else:
        for item in vacancies:
            elem = item['vacancy']
            await message.answer(format_vacancy(elem))


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
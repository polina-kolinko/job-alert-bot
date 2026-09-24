import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from aiogram.types import Message
from aiogram.filters import CommandStart

dp = Dispatcher()

@dp.message(CommandStart())
async def answer(message: Message):
    await message.answer("Привет! Я помогу искать новые вакансии.")

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
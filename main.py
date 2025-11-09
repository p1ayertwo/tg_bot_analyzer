import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_API_KEY
from bot.handlers import router


async def main():
    bot = Bot(token=TELEGRAM_API_KEY)
    dp = Dispatcher()

    dp.include_router(router)
    print("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

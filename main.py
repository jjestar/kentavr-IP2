import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
async def main():
    # Твой напарник чуть позже напишет хэндлеры (кнопки, команды)
    # и мы их подключим (зарегистрируем) прямо здесь:
    # from handlers import client
    # dp.include_router(client.router)

    print("working")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")
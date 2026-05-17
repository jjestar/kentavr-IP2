import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# 1. Импортируем твой роутер из хэндлеров
from handlers.client import router as client_router

# Настройка логирования для отслеживания работы бота в консоли
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def init_data_folder():
    """
    Проверяет наличие папки data и необходимых JSON файлов.
    Если их нет — создаёт, чтобы избежать ошибок FileNotFoundError.
    """
    os.makedirs("data", exist_ok=True)
    
    # Файл для истории (базово пустой список)
    if not os.path.exists("data/search_history.json"):
        with open("data/search_history.json", "w", encoding="utf-8") as f:
            f.write("[]")
            
    # Файл для избранного (базово пустой словарь)
    if not os.path.exists("data/favorites.json"):
        with open("data/favorites.json", "w", encoding="utf-8") as f:
            f.write("{}")


async def main():
    # 2. Инициализируем файлы данных перед стартом бота
    init_data_folder()

    # 3. Подключаем твой роутер с хэндлерами и кнопками
    dp.include_router(client_router)

    # Удаляем вебхуки, чтобы бот отвечал только на новые сообщения при перезапуске
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 Бот успешно запущен и готов к работе!")
    
    # Запуск пуллинга (опроса серверов Telegram)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Бот остановлен!")
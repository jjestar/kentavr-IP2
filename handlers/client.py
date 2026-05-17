from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Импортируем клавиатуры
from handlers.keyboards import get_main_menu, get_movie_actions
# Предполагаем, что Участник 1 напишет эти классы/функции
from services.movie_api import MovieAPI
from services.storage import Storage

router = Router()

# Определяем состояния для поиска
class SearchStates(StatesGroup):
    waiting_for_title = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Добро пожаловать в Movie Bot.\n"
        "Здесь ты можешь находить рейтинги IMDb фильмов и аниме.",
        reply_markup=get_main_menu()
    )

@router.message(F.text == "🔍 Поиск кино / аниме")
async def start_search(message: Message, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_title)
    await message.answer("Введите название фильма, сериала или аниме:")

@router.message(SearchStates.waiting_for_title)
async def process_search(message: Message, state: FSMContext):
    movie_title = message.text.strip()
    await state.clear() # Сбрасываем состояние поиска
    
    # 1. Сохраняем в историю (Вызов кода Участника 1 для Data Persistence)
    try:
        Storage.save_to_history(
            user_id=message.from_user.id, 
            username=message.from_user.username, 
            query=movie_title
        )
    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}") # Не ломаем бота, если JSON недоступен

    # 2. Делаем запрос к API (Вызов кода Участника 1)
    await message.answer("⏳ Ищу в базе данных IMDb...")
    
    try:
        # Допустим, метод возвращает объект класса Movie или Series (из папки models)
        media_item = MovieAPI.search_by_title(movie_title)
        
        if not media_item:
            await message.answer("❌ Ничего не найдено. Проверьте правильность названия.")
            return

        # Используем полиморфизм/методы классов из моделей для красивого вывода
        response_text = media_item.get_detailed_info() 
        
        # Отправляем ответ с Inline-кнопкой «Добавить в избранное»
        await message.answer(
            response_text, 
            reply_markup=get_movie_actions(imdb_id=media_item.imdb_id)
        )
        
    except Exception as e:
        # Критерий Robustness: бот не должен «падать» при ошибках сети или API
        await message.answer("⚠️ Произошла ошибка при обращении к серверу. Попробуйте позже.")
        print(f"Критическая ошибка поиска: {e}")

# Хэндлер для обработки нажатия инлайн-кнопки "Добавить в избранное"
@router.callback_query(F.data.startswith("fav_add:"))
async def handle_add_favorite(callback: CallbackQuery):
    imdb_id = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    try:
        # Вызов метода сохранения Участника 1
        Storage.save_to_favorites(user_id=user_id, imdb_id=imdb_id)
        # Отвечаем пользователю всплывающим окном в Telegram
        await callback.answer("✅ Успешно добавлено в избранное!", show_alert=True)
    except Exception as e:
        await callback.answer("❌ Не удалось сохранить.", show_alert=True)

@router.message(F.text == "📜 История поиска")
async def show_history(message: Message):
    try:
        history = Storage.get_user_history(message.from_user.id)
        if not history:
            await message.answer("Ваша история поиска пуста.")
            return
        
        text = "📜 Ваши последние запросы:\n" + "\n".join([f"- {item}" for item in history[-10:]])
        await message.answer(text)
    except Exception:
        await message.answer("Ошибка при чтении истории.")
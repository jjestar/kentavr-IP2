from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 1. Главное меню (Reply Keyboard)
def get_main_menu() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🔍 Поиск кино / аниме")],
        [KeyboardButton(text="⭐ Моё Избранное"), KeyboardButton(text="📜 История поиска")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb, 
        resize_keyboard=True, 
        input_field_placeholder="Выберите действие..."
    )

# 2. Кнопка под результатом поиска (Inline Keyboard)
def get_movie_actions(imdb_id: str) -> InlineKeyboardMarkup:
    # Передаем в callback_data уникальный префикс и id фильма, чтобы хэндлер понял, что произошло
    kb = [
        [InlineKeyboardButton(text="❤️ Добавить в избранное", callback_data=f"fav_add:{imdb_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
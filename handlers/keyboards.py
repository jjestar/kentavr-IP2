
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🔍 Search film")],
        [KeyboardButton(text="⭐ Favourite"), KeyboardButton(text="🕓 History")],
        [KeyboardButton(text="🔥 Popular")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Choose button",
    )
    return keyboard

def get_movie_keyboard(movie_id: int, is_fav: bool = False) -> InlineKeyboardMarkup:

    buttons = []

    if not is_fav:

        buttons.append([
            InlineKeyboardButton(
                text="❤️ Favourite",
                callback_data=f"fav_add:{movie_id}"
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="💔 delete from favourites",
                callback_data=f"fav_remove:{movie_id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_favourites_keyboard(movie_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="🗑 delete from favourites",
                callback_data=f"fav_remove:{movie_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from services import movie_api, storage
from models.movie import Movie
from handlers.keyboards import get_main_keyboard, get_movie_keyboard, get_favourites_keyboard

router = Router()

class MovieFormatter:
    @staticmethod
    def format_card(movie: Movie) -> str:
        return (
            f"🎬 <b>{movie.title}</b> ({movie.get_year()})\n"
            f"⭐ Rating: <b>{movie.rating}/10</b>\n"
            f"🎭 Genres: {movie.get_genres_string()}\n\n"
            f"📖 {movie.overview}"
        )

    @staticmethod
    def format_short(index: int, movie: Movie) -> str:
        return f"{index}. <b>{movie.title}</b> ({movie.get_year()}) — ⭐ {movie.rating}"
def format_movie_list(movies: list[Movie]):
    formatter = MovieFormatter()
    for index, movie in enumerate(movies, start=1):   # iterator
        yield formatter.format_short(index, movie)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Hi, <b>{message.from_user.first_name}</b>!\n\n"
        "I'll help you find any film information\n"
        "Just tell me name of the film and ill show you",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🆘 <b>How to use bot:</b>\n\n"
        "Click <b>🔍 Find film</b> and enter the name\n"
        "Click <b>🔥 Popular</b> I'll show you popular films\n"
        "Click <b>⭐ Favourite</b> - your favorite films\n"
        "Click <b>🕓 History</b> you film history",
        parse_mode="HTML",
    )
@router.message(F.text == "🔍 Поиск фильма")
async def btn_search(message: Message):
    await message.answer("✏️ Enter film or anime name:")


@router.message(F.text == "🔥 Популярные")
async def btn_popular(message: Message):
    movies = await movie_api.get_popular_movies()

    if not movies:
        await message.answer("😕 Cannot load popular films.")
        return

    # Собираем строки через генератор
    lines = list(format_movie_list(movies))
    text = "🔥 <b>Popular films right now:</b>\n\n" + "\n".join(lines)

    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "⭐ Favorite")
async def btn_favourites(message: Message):
    user_id = message.from_user.id
    movies = storage.get_favourites(user_id)

    if not movies:
        await message.answer("⭐ You have no favourite films")
        return

    await message.answer(f"⭐ <b>Your favourites ({len(movies)} ):</b>", parse_mode="HTML")
    for movie in movies:
        text = MovieFormatter.format_card(movie)
        keyboard = get_favourites_keyboard(movie.media_id)
        poster_url = movie.get_poster_url()
        if poster_url:
            await message.answer_photo(
                photo=poster_url,
                caption=text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "🕓 History")
async def btn_history(message: Message):
    user_id = message.from_user.id
    movies = storage.get_history(user_id)

    if not movies:
        await message.answer("🕓 History is empty")
        return

    # Генератор даёт нам строки одну за одной
    lines = list(format_movie_list(movies))
    text = "🕓 <b>Your history:</b>\n\n" + "\n".join(lines)

    await message.answer(text, parse_mode="HTML")

@router.message(F.text)
async def handle_search_query(message: Message):
    query = message.text.strip()
    wait_msg = await message.answer(f"🔍 looking for <b>{query}</b>...", parse_mode="HTML")

    movie = await movie_api.search_movie(query)

    await wait_msg.delete()

    if not movie:
        await message.answer(
            f"Couldnt find any film <b>{query}</b>.\n"
            "Try correcting name or write in English",
            parse_mode="HTML",
        )
        return

    storage.add_to_history(message.from_user.id, movie)
    user_id = message.from_user.id
    is_fav = storage.is_favourite(user_id, movie.media_id)

    text = MovieFormatter.format_card(movie)
    keyboard = get_movie_keyboard(movie.media_id, is_fav=is_fav)
    poster_url = movie.get_poster_url()

    if poster_url:
        await message.answer_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("fav_add:"))
async def callback_add_favourite(callback: CallbackQuery):

    movie_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    movie = await movie_api.get_movie_details(movie_id)

    if not movie:
        await callback.answer("Couldnt find the film", show_alert=True)
        return

    added = storage.add_to_favourites(user_id, movie)

    if added:
        new_keyboard = get_movie_keyboard(movie_id, is_fav=True)
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)

        await callback.answer(f"❤️ «{movie.title}» is now in favorite", show_alert=False)
    else:
        await callback.answer("Film is already in favorite", show_alert=False)


@router.callback_query(F.data.startswith("fav_remove:"))
async def callback_remove_favourite(callback: CallbackQuery):

    movie_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    removed = storage.remove_from_favourites(user_id, movie_id)

    if removed:

        is_from_favourites_list = "Your favorite films" in (callback.message.text or callback.message.caption or "")

        if is_from_favourites_list:
            await callback.message.edit_reply_markup(reply_markup=None)
        else:
            new_keyboard = get_movie_keyboard(movie_id, is_fav=False)
            await callback.message.edit_reply_markup(reply_markup=new_keyboard)

        await callback.answer("Film was deleted", show_alert=False)
    else:
        await callback.answer("Couldnt find it", show_alert=False)
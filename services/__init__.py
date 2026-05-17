from .movie_api import search_movie, get_movie_details, get_popular_movies
from .storage import (
    add_to_history, get_history, clear_history,
    add_to_favourites, remove_from_favourites, get_favourites, is_favourite,
)
__all__ = [
    "search_movie", "get_movie_details", "get_popular_movies",
    "add_to_history", "get_history", "clear_history",
    "add_to_favourites", "remove_from_favourites", "get_favourites", "is_favourite",
]
import json
import os
from models.movie import Movie
HISTORY_FILE = "data/history.json"
FAVOURITES_FILE = "data/favorites.json"
MAX_HISTORY = 20
def _load_file(filepath):
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


def _save_file(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def add_to_history(user_id, movie):
    data = _load_file(HISTORY_FILE)

    uid = str(user_id)

    if uid not in data:
        data[uid] = []

    user_history = data[uid]

    clean_history = []
    for m in user_history:
        if m["id"] != movie.media_id:
            clean_history.append(m)

    movie_dict = movie.to_dict()

    clean_history.insert(0, movie_dict)

    data[uid] = clean_history[:MAX_HISTORY]

    _save_file(HISTORY_FILE, data)


def get_history(user_id):
    data = _load_file(HISTORY_FILE)
    uid = str(user_id)

    if uid not in data:
        return []

    raw_list = data[uid]
    movie_objects = []

    for m in raw_list:
        obj = Movie(
            media_id=m["id"],
            title=m["title"],
            overview=m["overview"],
            release_date=m["release_date"],
            rating=m["rating"],
            genres=m["genres"],
            poster_path=m["poster_path"]
        )
        movie_objects.append(obj)

    return movie_objects
def add_to_favourites(user_id, movie):
    data = _load_file(FAVOURITES_FILE)
    uid = str(user_id)

    if uid not in data:
        data[uid] = []

    user_favs = data[uid]

    for m in user_favs:
        if m["id"] == movie.media_id:
            return False
    user_favs.append(movie.to_dict())
    data[uid] = user_favs

    _save_file(FAVOURITES_FILE, data)
    return True


def remove_from_favourites(user_id, movie_id):
    data = _load_file(FAVOURITES_FILE)
    uid = str(user_id)

    if uid not in data:
        return False

    user_favs = data[uid]
    new_favs = []
    was_deleted = False

    for m in user_favs:
        if m["id"] == movie_id:
            was_deleted = True
        else:
            new_favs.append(m)

    data[uid] = new_favs
    _save_file(FAVOURITES_FILE, data)
    return was_deleted


def get_favourites(user_id):
    data = _load_file(FAVOURITES_FILE)
    uid = str(user_id)

    if uid not in data:
        return []

    raw_list = data[uid]
    movie_objects = []

    for m in raw_list:
        obj = Movie(
            media_id=m["id"],
            title=m["title"],
            overview=m["overview"],
            release_date=m["release_date"],
            rating=m["rating"],
            genres=m["genres"],
            poster_path=m["poster_path"]
        )
        movie_objects.append(obj)

    return movie_objects


def clear_history(user_id):
    data = _load_file(HISTORY_FILE)
    uid = str(user_id)
    data[uid] = []

    _save_file(HISTORY_FILE, data)


def is_favourite(user_id, movie_id):
    data = _load_file(FAVOURITES_FILE)
    uid = str(user_id)

    if uid not in data:
        return False

    user_favs = data[uid]
    for m in user_favs:
        if m["id"] == movie_id:
            return True

    return False


def is_in_history(user_id, movie_id):
    data = _load_file(HISTORY_FILE)
    uid = str(user_id)

    if uid not in data:
        return False

    for m in data[uid]:
        if m["id"] == movie_id:
            return True
    return False
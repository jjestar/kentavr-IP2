import aiohttp
from config import API_KEY
from models.movie import Movie
TMDB_BASE_URL = "https://api.themoviedb.org/3"
async def search_movie(query, language="ru-RU"):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query,
        "language": language,
        "page": 1,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            # server returned error
            if resp.status != 200:
                return None
            data = await resp.json()

    results = data.get("results", [])
    if not results:
        return None
    first_movie = results[0]

        return await get_movie_details(first_movie["id"], language=language)


async def get_movie_details(movie_id, language="ru-RU"):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": language,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return None
            raw = await resp.json()
    genres_list = []
    for g in raw.get("genres", []):
        genres_list.append(g["name"])
    return Movie(
        media_id=raw["id"],
        title=raw.get("title", ""),
        overview=raw.get("overview", "Описание отсутствует."),
        release_date=raw.get("release_date", ""),
        rating=round(raw.get("vote_average", 0.0), 1), # rounding rating
        genres=genres_list,
        poster_path=raw.get("poster_path")
    )


async def get_popular_movies(language="ru-RU", page=1):
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": language,
        "page": page,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()

    movies_list = []
    for raw in data.get("results", [])[:10]:
        obj = Movie(
            media_id=raw["id"],
            title=raw.get("title", ""),
            overview=raw.get("overview", "Описание отсутствует."),
            release_date=raw.get("release_date", ""),
            rating=round(raw.get("vote_average", 0.0), 1),
            genres=[],
            poster_path=raw.get("poster_path")
        )
        movies_list.append(obj)

    return movies_list
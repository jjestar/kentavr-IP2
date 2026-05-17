from models.media import Media
class Movie(Media):
    def __init__(self, media_id, title, overview, release_date, rating, genres, poster_path):
        super().__init__(media_id, title, overview, release_date, rating)
        self.genres = genres
        self.poster_path = poster_path

    def get_poster_url(self):
        if self.poster_path:
            return "https://image.tmdb.org/t/p/w500" + self.poster_path
        return None

    def get_genres_string(self):
        if self.genres:
            return ", ".join(self.genres)
        return "-"

    def to_dict(self):
        return {
            "id": self.media_id,
            "title": self.title,
            "overview": self.overview,
            "release_date": self.release_date,
            "rating": self.rating,
            "genres": self.genres,
            "poster_path": self.poster_path
        }
class Media:
    def __init__(self, media_id, title, overview, release_date, rating):
        self.media_id = media_id        # ID фильма
        self.title = title              # Название
        self.overview = overview        # Описание
        self.release_date = release_date  # Дата релиза
        self.rating = rating            # Рейтинг

    def get_year(self):
        if self.release_date and len(self.release_date) >= 4:
            return self.release_date[:4]
        return "N/A"
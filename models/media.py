class Media:
    def __init__(self, media_id, title, overview, release_date, rating):
        self.media_id = media_id
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.rating = rating

    def get_year(self):
        if self.release_date and len(self.release_date) >= 4:
            return self.release_date[:4]
        return "n/a"
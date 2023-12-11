from django.db import models

class Genre(models.Model):

    description = models.TextField()

    # list comprehension within Genre model to define songs field(related name on the foreign key in SongGenre model is now song_genres) and import the SongSerializer into the Genre view. This basically removes the forgeign key header from the data in postman where it doesnt need to be:
    def songs(self):
        return [song_genre.song_id for song_genre in self.song_genres.all()]

from django.db import models
from .genre import Genre
from .song import Song

class SongGenre(models.Model):

    song_id = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="genre_songs")
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="song_genres")

# Note - if using serializers to join data sets and models together, the related_name=" " query set must be added into the join table model so Django ORM can correctly fetch the appropriate data from the desired tables. Otherwise you can correctly setup your serializers and they still will not call and display the data.

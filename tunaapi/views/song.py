"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, SongGenre, Genre
from django.utils.dateparse import parse_duration


class SongView(ViewSet):
    """Tuna api song view"""
    def retrieve(self, request, pk):
      """Handle GET requests for single song
      Returns:
          Response -- JSON serialized song
      """
      try:  
          song = Song.objects.get(pk=pk)
          serializer = SongSerializer(song)
          return Response(serializer.data, status=status.HTTP_200_OK)
      except Song.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    
    def list(self, request):
      """Handle GET requests to get all songs
      Returns:
          Response -- JSON serialized list of songs
      """
      songs = Song.objects.all()
      
      # filter to query songs by artist_id
      artist = request.query_params.get('artist_id', None)
      if artist is not None:
          songs = songs.filter(artist_id_id=artist)
   
      # filter to query songs by genre_id
      requested_genre = request.query_params.get('genre_id', None)
      if requested_genre is not None:
          songs = Song.objects.filter(genres__genre_id__id=requested_genre)
        
      serializer = SongSerializer(songs, many=True)
      return Response(serializer.data)
    
    
    def create(self, request):
      """Handle POST operations for songs
      Returns 
          Response -- JSON serialized song instance
      """
      artist_id = Artist.objects.get(pk=request.data["artistId"])
      song = Song.objects.create(
        title=request.data["title"],
        album=request.data["album"],
        length=parse_duration(request.data["length"]),
        artist_id=artist_id,
      )
      serializer = SongSerializer(song)
      return Response(serializer.data)
    
    
    def update(self, request, pk):
        """Handle PUT requests for a song
        Returns:
            Response -- Empty body with 204 status code
        """
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = parse_duration(request.data["length"])
        
        artist_id = Artist.objects.get(pk=request.data["artistId"])
        song.artist_id = artist_id
        song.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
      
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

        
class SongGenreSerializer(serializers.ModelSerializer):
  class Meta:
      model = SongGenre
      fields = ('genre_id', )
      depth = 1
      
class SongSerializer(serializers.ModelSerializer):
  """JSON serializer for songs"""
  genres = SongGenreSerializer(many=True, read_only=True)
  
  class Meta:
      model = Song
      fields = ('id', 'title', 'artist_id', 'album', 'length', 'genres')
      depth = 1

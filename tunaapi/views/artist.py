"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist
from django.db.models import Count



class ArtistView(ViewSet):
    """Tuna api artist view"""
    
    def retrieve(self, request, pk):
      """Handle GET requests for single artist
      Returns:
        Response -- JSON serialized artist
      """
      try:
          artist = Artist.objects.get(pk=pk)
          # artist = Artist.objects.annotate(song_count=Count('songs')).get(pk=pk)
          serializer = ArtistSerializer(artist)
          return Response(serializer.data, status=status.HTTP_200_OK)
      except Artist.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
      
    def list(self, request): 
      """Handle GET requests to get all artists
      Returns:
          Response -- JSON serialized list of artists
      """
      artists = Artist.objects.all()
      # artists = Artist.objects.annotate(song_count=Count('songs')).all()
      
      # filter to query artists by genre_id
      # requested_genre = request.query_params.get('genre_id', None)
      # if requested_genre is not None:
      #   artists = Artist.objects.filter(songs__genres__genre_id=requested_genre)
      serializer = ArtistSerializer(artists, many=True)
      # return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.data)
    
    
    def create(self, request):
      """Handle POST operations for artists
      Returns 
          Response -- JSON serialized artist instance
      """
      artist = Artist.objects.create(
        name=request.data["name"],
        age=request.data["age"],
        bio=request.data["bio"],
      )
      serializer = ArtistSerializer(artist)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, pk):
      """Handle PUT requests for an artist
      Returns:
          Response -- Empty body with 204 status code
      """
      
      artist = Artist.objects.get(pk=pk)
      artist.name = request.data["name"]
      artist.age = request.data["age"]
      artist.bio = request.data["bio"]
      artist.save()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk):
      """Handle DELETE request for an artist"""
      artist = Artist.objects.get(pk=pk)
      artist.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer(serializers.ModelSerializer):
  """JSON serializer for artists"""
  song_count = serializers.IntegerField(default=None)
  class Meta:
      model = Artist
      fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
      depth = 1
      
# class ArtistSongsSerializer(serializers.ModelSerializer):
#   """JSON serializer to get artist's associated songs"""
#   songs = SongSerializer(many=True, read_only=True)
  
#   class Meta:
#     model = Artist
#     fields = ('id', 'name', 'age', 'bio', 'songs', )
#     depth = 1

# class AllArtistSerializer(serializers.ModelSerializer):
#   """JSON serializer for artists with no song info"""
#   class Meta:
#       model = Artist
#       fields = ('id', 'name', 'age', 'bio')

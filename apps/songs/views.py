from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from apps.songs.models import *
from apps.songs.serializers import *
from django.shortcuts import get_object_or_404
from apps.songs.signals import song_added_to_album
# Create your views here.

    
class ScheduleSongView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        song_serializer = SongSerializer(data=request.data)
        if song_serializer.is_valid():
            song = song_serializer.save()

            scheduled_song_data = {
                'song': song.id,
                'scheduled_time': request.data.get('scheduled_time'),
                'created_by': request.user.id
            }
            scheduled_song_serializer = ScheduledSongSerializer(data=scheduled_song_data)
            if scheduled_song_serializer.is_valid():
                scheduled_song_serializer.save()
                return Response({'message': 'Song scheduled successfully'}, status=status.HTTP_201_CREATED)
            
            song.delete()
            return Response(scheduled_song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AllSongsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SearchSongsView(APIView):

    def get(self, request, format=None):
        query = request.GET.get('query') 
        tag = request.GET.get('tag')
        
        if not query and not tag:
            return Response({'message': 'Please provide a query or a tag.'}, status=status.HTTP_400_BAD_REQUEST)
        
        songs = Song.objects.all()
        
        if query:
            songs = songs.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        
        if tag:
            songs = songs.filter(tags__icontains=tag)
        
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LikeSongView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, song_id, format=None):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user in song.liked_by.all():
            return Response({'message': 'You have already liked this song'}, status=status.HTTP_400_BAD_REQUEST)
        
        song.likes += 1
        song.liked_by.add(request.user)
        song.save()
        
        return Response({'message': 'Song liked successfully'}, status=status.HTTP_200_OK)
    

    
class AlbumCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        albums = Album.objects.filter(user=user)
        album_serializer = AlbumSerializer(albums, many=True)
        return Response(album_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        album_serializer = AlbumCreateSerializer(data=request.data)
        if album_serializer.is_valid():
            album = album_serializer.save(user=request.user)
            return Response({'message': 'Album created successfully'}, status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSongsToAlbumView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id, format=None):
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({'message': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddSongsToAlbumSerializer(data=request.data)
        if serializer.is_valid():
            song_ids = serializer.validated_data.get('song_ids', [])
            songs = Song.objects.filter(id__in=song_ids)

            songs_added = []
            songs_already_in_album = []

            for song in songs:
                if song not in album.songs.all():
                    album.songs.add(song)
                    songs_added.append(song)
                    song_added_to_album.send(sender=self.__class__, song=song, album=album)
                else:
                    songs_already_in_album.append(song)

            response_data = {}
            if songs_added:
                response_data['message'] = f'{len(songs_added)} songs added to the album.'
            if songs_already_in_album:
                response_data['message_already_in_album'] = f'{len(songs_already_in_album)} songs are already in the album.'

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id, format=None):
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment = comment_serializer.save(user=request.user, song=song)
            return Response({'message': 'Comment added successfully', 'comment': CommentSerializer(comment).data}, status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SongsAddFavourite(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request,songs_id):

        fav = Favorite.objects.filter(songs__id=songs_id,user = self.request.user)
        if fav.exists():
            serializer = FavouriteSerialzier(fav, many = True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,songs_id):

        songs = Song.objects.get(id= songs_id)
        user = self.request.user
        new_fav = Favorite.objects.create(songs = songs,user=user)
        serializer = FavouriteSerialzier(new_fav, data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



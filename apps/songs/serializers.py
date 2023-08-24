from rest_framework import serializers
from apps.songs.models import *
from apps.account.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']


class SongSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['id','title','artist','release_date', 'comments', 'likes']


class ScheduledSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledSong
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'description', 'is_public', 'songs']


class AlbumCreateSerializer(serializers.ModelSerializer):
    songs = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Album
        fields = ['title', 'description','is_public', 'songs']

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        for song_id in songs_data:
            song = Song.objects.get(id=song_id)
            album.songs.add(song)
        return album


class AlbumSongSerializer(serializers.Serializer):
    song_ids = serializers.ListField(child=serializers.IntegerField())


class AddSongsToAlbumSerializer(serializers.Serializer):
    song_ids = serializers.ListField(child=serializers.IntegerField())


class FavouriteSerialzier(serializers.ModelSerializer):

    songs = SongSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta: # pylint: disable=too-few-public-methods

        """In class Meta model Favorite is used and its field songs,user and id"""

        model = Favorite
        fields = ['songs','user','id']



from django.urls import path
from apps.songs.views import * 
urlpatterns = [
    path('schedule-song/', ScheduleSongView.as_view(), name='schedule-song'),
    path('all-songs/', AllSongsView.as_view(), name='all-songs'),
    path('search-songs/', SearchSongsView.as_view(), name='search-songs'),
    path('like-song/<int:song_id>/', LikeSongView.as_view(), name='like-song'),
    path('albums/', AlbumCreateView.as_view(), name='album-list'),
    path('add-songs-to-album/<int:album_id>/', AddSongsToAlbumView.as_view(), name='add-songs-to-album'),
    path('songs/<int:song_id>/add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('songs/<int:songs_id>/fav/',SongsAddFavourite.as_view()),

]
from django.db import models
from apps.account.models import User
from django.contrib.auth import get_user_model
# Create your models here.


class Song(models.Model):
    
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    release_date = models.DateField()
    tags = models.CharField(max_length=255, blank=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_songs', blank=True)

    def __str__(self):
        return self.title


class ScheduledSong(models.Model):
    
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='scheduled_songs')

    def __str__(self):
        return f"Scheduled song: {self.song} at {self.scheduled_time}"
    

class Album(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField(default=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, related_name='albums', blank=False)
    
    def __str__(self):
        return self.title



class Comment(models.Model):
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.song} at {self.created_at}"

class Favorite(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    songs = models .ForeignKey(Song,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        return '{self.songs.song_name}'.format(self=self)



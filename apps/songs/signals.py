from django.db.models.signals import Signal
from django.dispatch import receiver
from apps.songs.models import Song
from apps.account.models import User

song_added_to_album = Signal()

@receiver(song_added_to_album)
def send_notification_on_song_added(sender, song, album, **kwargs):

    followers = album.followers.all()
    for follower in followers:
        notification_message = f"New song '{song.title}' added to album '{album.title}'."
        follower.notifications.append(notification_message)
        follower.save()

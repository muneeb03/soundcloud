from django.contrib import admin
from apps.songs.models import *
# Register your models here.

admin.site.register(Song)
admin.site.register(ScheduledSong)
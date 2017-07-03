import os
from mpd import MPDClient

from django.db import models, transaction
from django.dispatch import receiver

from .models import Track, PlaylistTrack

from .methods.playlist import play, update_playlist_stats

def _delete_file(filename):
    filepath = os.path.join("/home/mpd/music", os.path.basename(filename))
    if os.path.isfile(filepath):
        os.remove(filepath)
        print("File deleted: %s" % filepath)


@receiver(models.signals.post_delete, sender=Track)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes audiofile on `post_delete` """
    if instance.filename:
        _delete_file(instance.filename)

@receiver(models.signals.post_save, sender=PlaylistTrack)
def play_track(sender, instance, *args, **kwargs):
    transaction.on_commit(play)
    transaction.on_commit(update_playlist_stats)


from mpd import MPDClient
import time

from radio.models import Track, PlaylistTrack
from .youtube import get_track_from_youtube

def add_track_to_queue(filename):
    client = MPDClient()
    client.connect('localhost', 6601)
    client.update(filename)
    time.sleep(0.5)
    client.add(filename)
    client.play()
    client.close()

def update_track(track_id, **kwargs):
    Track.objects.filter(pk=track_id).update(**kwargs)

def get_track_from_cache(source, source_id):
    return Track.objects.filter(source=source, source_id=source_id).first()

def add_track_to_playlist(track_id, comment, sender_ip):
    ptrack = PlaylistTrack.objects.filter(track__id=track_id).first()
    track = Track.objects.get(pk=track_id)
    if ptrack is None:
        ptrack = PlaylistTrack(
            track=track,
            comment=comment,
            sender_ip=sender_ip
        )
        ptrack.save()
    else:
        print("Already requested: %s from %s" % (track.filename, sender_ip))
    return ptrack

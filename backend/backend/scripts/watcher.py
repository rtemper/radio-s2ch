from mpd import MPDClient
from backend.asgi import channel_layer
from radio.methods.hosts import get_unique_listeners
import redis
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
from radio.models import Track, PlaylistTrack
from radio.methods.playlist import next_track, get_playlist_stats

# Setup global redis instance to store song info.
# Most of data goes through websocket, but we need
# some kind of storage to send song info for new clients
# that doesn't got events yet
r = redis.StrictRedis(
    os.environ.get("R_REDIS_HOST", "localhost"),
    os.environ.get("R_REDIS_PORT", "6379"),
    db=os.environ.get("R_REDIS_HOSTINFO_DB", "2")
)
# check redis connection before the start
r.get(None)


def notify_clients(song_name, song_author, song_comment, listeners_count,
                   query_size, unique_senders):
    actions = [{
        'type': 'CHANGE_TRACK_NAME',
        'name': song_name,
        'author': song_author
    }, {
        'type': 'CHANGE_TRACK_COMMENT',
        'comment': song_comment
    }, {
        'type': 'SET_UNIQUE_LISTENERS',
        'count': listeners_count
    }, {
        'type': 'SET_QUERY_SIZE',
        'size': query_size,
    }, {
        'type': 'SET_UNIQUE_SENDERS',
        'count': unique_senders
    }]
    for action in actions:
        channel_layer.send('radio-events', action)


def get_track_by_filename(filename):
    return Track.objects.filter(filename=filename).first()


def listen_mpd_events():

    last_track_filename = None
    last_mpd_state = None

    client = MPDClient()
    client.connect('mpd', 6601)
    print("Connected to MPD daemon, listening...")

    ev = None
    while(True):

        current_track_filename = client.currentsong().get('file', None)
        current_mpd_state = client.status()['state']
        track = get_track_by_filename(current_track_filename)

        track_changed = current_track_filename != last_track_filename
        state_changed = current_mpd_state != last_mpd_state
        player_just_stopped = track_changed and state_changed and (track is None)

        print("MPD event %s, track_changed: %s, state_changed: %s, track: %s" % (
            ev, track_changed, state_changed, track
        ))

        if player_just_stopped:
            next_track()
            # this dont remove last PlaylistTrack yet
            # (if there is no more tracks)

        # the only way to know does song changed or not
        # is to compare its value before and after event.
        elif track_changed:

            # if song changed we need to do some routines.

            # hack around django post_save() signal that
            # doesn't act immidiately.
            # import time
            # time.sleep(2)

            # Remove old PlaylistTrack from database
            ptrack = PlaylistTrack.objects.filter(
                status='p',
                track__filename=last_track_filename
            ).first()
            if ptrack is not None:
                ptrack.delete()

            # Mark current PlaylistTrack as 'playing'
            ptrack = PlaylistTrack.objects.filter(
                status='q',
                track__filename=current_track_filename
            ).first()
            if ptrack:
                ptrack.status = 'p'
                ptrack.save()

            # Get unique listeners
            listeners_count = get_unique_listeners()

            # Get playlist stats
            query_size, unique_senders = get_playlist_stats()

            # Nofify clients
            notify_clients(
                song_name=track.name,
                song_author=track.author,
                song_comment=(ptrack.comment if ptrack else ''),
                listeners_count=listeners_count,
                query_size=query_size,
                unique_senders=unique_senders
            )

            # send song to redis
            r.set('song_name', track.name)
            r.set('song_author', track.author)
            r.set('song_comment', ptrack.comment if ptrack else '')

            # 5)Mark current track as previous, as it already in mpd
            last_track_filename = current_track_filename

        # at this moment script waits for incoming events
        # ev = client.idle('playlist','player')
        ev = client.idle('player')


if __name__ == "__main__":
    listen_mpd_events()




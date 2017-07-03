import os
import redis

from django.db.models import Case, When
from mpd import MPDClient, CommandError
from channels import Channel

from radio.models import Track, PlaylistTrack
from .hosts import get_most_inactive_hosts, mark_host_as_recently_active

MPD_HOST = os.environ.get("R_MPD_HOST", "127.0.0.1")
MPD_PORT = int(os.environ.get("R_MPD_PORT", 6601))

# Setup global redis instance to recive song info.
r = redis.StrictRedis(
    os.environ.get("R_REDIS_HOST", "localhost"),
    os.environ.get("R_REDIS_PORT", "6379"),
    db=os.environ.get("R_REDIS_HOSTINFO_DB", "2")
)
# check redis connection before the start
r.get(None)


""" Exceptions """

class PlaylistError(Exception):
    """Basic exception for errors raised by playlist"""
    def __init__(self, playlist, msg=None):
        if msg is None:
            msg = "An error occured with playlist operation"
        super(PlaylistError, self).__init__(msg)
        self.playlist = playlist

class EmptyPlaylistError(PlaylistError):
    def __init__(self):
        msg = "Operation failed in cause of empty playlist"
        super(EmptyPlaylistError, self).__init__(self, msg)

class TrackNotFoundError(PlaylistError):
    def __init__(self, filename):
        msg = "Track was not found in a database: %s" % filename
        super(TrackNotFoundError, self).__init__(self, msg)


""" Methods """

def add_playlist_track_to_mpd(ptrack):
    filename = ptrack.track.filename
    client = MPDClient()
    client.connect(MPD_HOST, MPD_PORT)
    try:
        client.add(filename)
        client.play()
    except CommandError as e:
        raise TrackNotFoundError(filename)


def get_unique_hosts():
    return PlaylistTrack.objects.filter(status='q').order_by('sender_ip')\
        .distinct('sender_ip').values_list('sender_ip', flat=True)


# def get_track_candidates(limit=None):
#     """Get first candidate for playing from each host"""
#     if limit is None:
#         limit = len(get_unique_hosts())
#     track_ids = PlaylistTrack.objects.order_by('sender_ip', 'id')\
#         .distinct('sender_ip').values_list('id', flat=True)
#     candidates = PlaylistTrack.objects.filter(id__in=track_ids).order_by('id')[:limit]
#     return candidates


def get_playlist_stats():
    """Get number of unique senders and number
    of tracks from the playlist"""
    unique_senders = PlaylistTrack.objects\
        .exclude(status='p').exclude(sender_ip='127.0.0.2')\
        .distinct('sender_ip').count()
    query_size = PlaylistTrack.objects\
        .exclude(status='p').exclude(sender_ip='127.0.0.2').count()
    r.set('query_size', query_size)
    r.set('unique_senders', unique_senders)
    return query_size, unique_senders

def update_playlist_stats():
    query_size, unique_senders = get_playlist_stats()
    actions = [{
        'type': 'SET_QUERY_SIZE',
        'size': query_size
    },{
        'type': 'SET_UNIQUE_SENDERS',
        'count': unique_senders
    }]
    for action in actions:
        Channel('radio-events').send(action)

def get_playlist_stats_from_cache():
    query_size = r.get('query_size')
    query_size = query_size.decode() if query_size else ''
    unique_senders = r.get('unique_senders')
    unique_senders = unique_senders.decode() if unique_senders else ''
    return query_size, unique_senders



def get_best_candidate():
    """Get track from most inactive host.
    Draws are resolved by id (FIFO)"""
    hosts = get_most_inactive_hosts(get_unique_hosts())
    ptrack = PlaylistTrack.objects.filter(sender_ip__in=hosts, status='q')\
        .order_by('id').first()
    return ptrack

def next_track():

    if not PlaylistTrack.objects.filter(status='q').exists():

        # get last played PlaylistTrack if any
        last_ptracks = PlaylistTrack.objects.filter(status='p')
        last_tracks_ids = [ pt.track.id for pt in last_ptracks ]

        # suggest replacement for this track
        track = Track.objects.filter(status='r') \
                             .exclude(id__in=last_tracks_ids).order_by('?')[0]

        # delete last played PlaylistTracks
        if last_ptracks:
            last_ptracks.delete()

        # suggest a new track (random) to fill playlist
        # track = Track.objects.filter(status='r').order_by('?')[0]
        ptrack = PlaylistTrack(
            track=track,
            sender_ip='127.0.0.2',
            comment='sponsored by localhost'
        )
        ptrack.save()
        # dont need to add track manualy, since
        # we have post_save() signal on PlaylistTrack

    else:
        ptrack = get_best_candidate()
        add_playlist_track_to_mpd(ptrack)
        mark_host_as_recently_active(ptrack.sender_ip)


def play():
    c = MPDClient()
    c.connect(MPD_HOST, MPD_PORT)
    status = c.status()['state']
    if status == 'stop':
        next_track()


def get_current_track_info():
    name = r.get('song_name')
    author = r.get('song_author')
    comment = r.get('song_comment')
    name = name.decode() if name else 'Unknown'
    author = author.decode() if author else ''
    comment = comment.decode() if comment else ''
    return name, author, comment

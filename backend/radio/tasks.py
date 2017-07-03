from backend.celery import app

from .models import Track
from .methods.tracks import \
    get_track_from_cache, add_track_to_playlist, update_track
from .methods.youtube import get_track_from_youtube, extract_metadata, YoutubeDownloadError

@app.task
def add_to_queue_from_youtube(youtube_id, comment, sender_ip):
    track = get_track_from_cache('y', youtube_id)
    if track is None:
        print("Track %s is not in cache, downloading..." % youtube_id)
        track = Track(
            source='y',
            source_id=youtube_id
        )
        track.save()

        def download_success_handler(filename):
            author, name = extract_metadata(filename)
            update_track(
                track_id=track.id,
                author=author,
                name=name,
                filename=filename,
                status='r'
            )
            add_track_to_playlist(track.id, comment, sender_ip)

        def download_error_handler(video_id):
            track.delete()

            # notify clients about an error
            # FIXME
            #

            print("error occurs during upload: video does not exist")

        try:
            get_track_from_youtube(
                youtube_id, download_success_handler, download_error_handler
            )

        except YoutubeDownloadError as e:
            author, name = extract_metadata(e.filename)
            update_track(
                track_id=track.id,
                author=author,
                name=name,
                filename=e.filename,
                status='e'
            )
    else:
        print("Track %s is found in cache, adding to playlist directly" % youtube_id)
        # add_track_to_queue(track.filename)
        add_track_to_playlist(track.id, comment, sender_ip)

import os
import youtube_dl
import shutil
import mutagen

MAX_FILE_SIZE = int(os.environ.get('R_MAX_YOUTUBE_FILE_SIZE', 10000000))
MPD_MUSIC_CATALOG = os.environ.get('R_MPD_MUSIC_CATALOG', '/home/mpd/music')


class YoutubeDownloadError(Exception):
    """Youtube file cannot be downloaded due to limits"""
    def __init__(self, msg=None, filesize=0, filename=''):
        if msg is None:
            msg = "Youtube file cannot be downloaded due to limits"
        super(YoutubeDownloadError, self).__init__(msg)
        self.msg = msg
        self.filesize = filesize
        self.filename = filename

    def __str__(self):
        return "%s: %s bytes for %s" % (
            self.msg, self.filesize, self.filename )


def stop_asap_if_limit_reached(d):
    """ Stop active download if resulting video is too big"""

    # m4a containers don't support total_bytes value
    # we need to download MAX_FILE_SIZE bytes before stop
    m4a_test_passed = 'fragment_count' in d and d['downloaded_bytes'] > MAX_FILE_SIZE

    # if total_bytes is presented we can interrupt session early
    default_test_passed = 'total_bytes' in d and d['total_bytes'] > MAX_FILE_SIZE

    if m4a_test_passed or default_test_passed:
        print("file too large")
        os.remove("%s.part" % d['filename'])
        raise YoutubeDownloadError(
            msg="Requested file is too big",
            filesize=d['total_bytes'],
            filename=d['filename']
        )

def stop_if_too_long(d):
    f = mutagen.File(d['filename'])
    if f is not None:
        file_length = f.info.length
        if file_length > 420:
            raise YoutubeDownloadError(
                msg="Requested file is too long",
                filename=d['filename']
            )

def get_track_from_youtube(video_id, onSuccess, onError):

    def status_hook(d):
        print(d)

        if d['status'] == 'downloading':
            stop_asap_if_limit_reached(d)

        if d['status'] == 'finished':

            # last check for audio length
            stop_if_too_long(d)

            src = os.path.join(os.getcwd(), d['filename'])
            filename = d['filename']
            dst = os.path.join(MPD_MUSIC_CATALOG, filename)
            shutil.move(src, dst)
            os.chmod(dst, 0o755)
            onSuccess(filename)

        if d['status'] == 'error' and onError:
            onError(video_id)

    ydl_opts = {
        'format': 'bestaudio',
        'progress_hooks': [status_hook],
        'fixup': 'never'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([
                f'http://www.youtube.com/watch?v={video_id}'
            ])
        except youtube_dl.utils.DownloadError as e:
            onError(e)


def extract_metadata(filename):
    # cut extension and youtube_id from the end
    raw = filename.rsplit('.', 1)[0][:-12]
    print(raw)
    if ' - ' in raw:
        author, name = raw.split(' - ', 1)
    elif '- ' in raw:
        author, name = raw.split('- ', 1)
    elif '—' in raw:
        author, name = raw.split('—', 1)
    else:
        author, name = '', raw
    return author, name


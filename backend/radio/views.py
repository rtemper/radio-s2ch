import os
import shutil

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from mpd import MPDClient
import mutagen

from radio.models import Track, PlaylistTrack
from .methods.tracks import add_track_to_queue
from .tasks import add_to_queue_from_youtube

from .serializers import YoutubeRequestSerializer, FileRequestSerializer

MPD_MUSIC_CATALOG = os.environ.get('R_MPD_MUSIC_CATALOG', '/home/mpd/music')


""" Playlist methods """

class AddToPlaylistFromYoutube(APIView):
    """Add track to playlist by it's youtube ID"""
    def post(self, request, *args, **kwargs):
        serializer = YoutubeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # FIXME check client limits before task creating

        add_to_queue_from_youtube.delay(
            sender_ip=request.META.get('HTTP_X_REAL_IP', "0.0.0.0"),
            **serializer.data
        )

        return Response(serializer.data)


class AddToPlaylistFromFile(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = request.data['file']

        filename = "file-%s" % uploaded_file.name
        source_id = "file-%s" % uploaded_file.size # replace by file hash if required

        # Add track if not exist
        cached_track = Track.objects.filter(source_id=source_id).first()
        if not cached_track:
            with default_storage.open(filename, 'wb+') as dst:
                for chunk in uploaded_file.chunks():
                    dst.write(chunk)
            os.chmod(default_storage.path(filename), 0o755)

            track = Track(
                source='f',
                source_id=source_id,
                name=serializer.data.get('name'),
                author=serializer.data.get('author'),
                filename=filename,
                status='r'
            )
            track.save()
        else:
            track = cached_track

        # Add track to playlist if not exist
        cached_request = PlaylistTrack.objects.filter(track=track).first()
        if not cached_request:
            ptrack = PlaylistTrack(
                track=track,
                comment=request.data.get('comment'),
                sender_ip=request.META.get('HTTP_X_REAL_IP', "0.0.0.0"),
            )
            ptrack.save()
            return Response(ptrack.created_at)
        return Response(cached_request.created_at)


class GetRequestedTracks(APIView):
    def get(self, request, *args, **kwargs):
        sender_ip = request.META.get('HTTP_X_REAL_IP', "0.0.0.0")
        user_requests = PlaylistTrack.objects.filter(
            sender_ip=sender_ip
        ).order_by('id')
        result = []
        for request in user_requests:
            result.append({
                "name": request.track.name,
                "author": request.track.author,
                "comment": request.comment,
                "status": request.track.status,
                "type": request.track.source
            })
        return Response(result)


def uuid_in_post_required(cls):
    def decorate(fn):
        def wrapper(self, request, *args, **kwargs):
            print("Post intercepted")
            result = fn(self, request, *args, **kwargs)
            print("Clear up")
            return result
        return wrapper
    cls.post = decorate(cls.post)
    return cls

from rest_framework import serializers
class TestSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(required=True)

@uuid_in_post_required
class SessionTest(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.session.session_key:
        #     request.session.create()
        print("post touched")
        return Response("ok")



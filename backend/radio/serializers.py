from rest_framework import serializers
import mutagen
import taglib
import os

class YoutubeRequestSerializer(serializers.Serializer):
    youtube_id = serializers.CharField()
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_youtube_id(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Wrong youtube ID")
        return value

class FileRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    comment = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def validate_file(self, value):
        try:
            file_length = mutagen.File(value).info.length
        except AttributeError:
            raise serializers.ValidationError("Unknown format")
        if file_length > 480:
            raise serializers.ValidationError("Audio is too long")
        return value

    def __aggregate_metadata(self, data):
        """Set appropriate metadata for Track instance
        based on multiple tag sources (file and user input)"""
        f = data['file']
        filename = "/tmp/%s" % f.name
        with open(filename, 'wb+') as dst:
            for chunk in f.chunks():
                dst.write(chunk)
        meta = taglib.File(filename)
        os.remove(filename)

        tag_title = meta.tags.get('TITLE', [None])[0]
        tag_author = meta.tags.get('ARTIST', [None])[0]

        user_title = data.get('name', None)
        user_author = data.get('author', None)

        title = None
        author = None

        title = user_title if user_title else tag_title
        author = user_author if user_author else tag_author

        if not title and not author:
            print("Neither title nor author")
            raise serializers.ValidationError("Name or author required")

        if not title:
            title = ''
        if not author:
            author = ''

        data['name'] = title
        data['author'] = author
        return data

    def validate(self, data):
        return self.__aggregate_metadata(data)




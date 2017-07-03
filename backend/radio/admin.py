from django.contrib import admin
from django.utils.html import format_html
from .models import Track, PlaylistTrack

STATUS_COLORS = {
    'i': 'cdcd00',
    'p': 'ccdcd0',
    'r': '006400',
    'e': 'ff0000'
}

STATUS_CHOICES = {
    'i': 'Initiating',
    'p': 'Processing',
    'r': 'Ready',
    'e': 'Error'
}

class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'source', 'colored_status']

    def colored_status(self, obj):
        return format_html(
            '<span style="color: #%s;">%s</span>' % (
                STATUS_COLORS[obj.status],
                STATUS_CHOICES[obj.status]
            )
        )
    colored_status.short_description = 'status'




class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ['get_author', 'get_name', 'status', 'sender_ip', 'comment']

    def get_name(self, obj):
        return obj.track.name
    get_name.short_description='Name'

    def get_author(self, obj):
        return obj.track.author
    get_author.short_description='Author'



admin.site.site_header = 'Radio #s2ch'
admin.site.register(Track, TrackAdmin)
admin.site.register(PlaylistTrack, PlaylistTrackAdmin)

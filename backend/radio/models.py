import os
from django.db import models

class Track(models.Model):
    SOURCE_CHOICES = (
        ('y', 'Youtube'),
        ('f', 'User file')
    )
    STATUS_CHOICES = (
        ('i', "Initiating"),
        ('p', "Processing"),
        ('r', "Ready"),
        ('e', "Error")
    )
    name = models.CharField(max_length=255, blank=True, default='')
    author = models.CharField(max_length=128, blank=True, default='')
    filename = models.CharField(max_length=255, blank=True, default='')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='i')
    source = models.CharField(max_length=1, choices=SOURCE_CHOICES)
    source_id = models.CharField(max_length=255, blank=True, default='')
    votes_up = models.IntegerField(default=0)
    votes_down = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.author, self.name)


class PlaylistTrack(models.Model):
    STATUS_CHOICES = (
        ('q', 'Queried'),
        ('p', 'Playing')
    )
    track = models.ForeignKey(Track)
    sender_ip = models.GenericIPAddressField(protocol='IPv4')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True, default='')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='q')

    def __str__(self):
        # probably not optimized lookups
        # FIXME later
        return "%s: %s - %s" % (self.sender_ip, self.track.author, self.track.name)

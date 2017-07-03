from channels.generic.websockets import JsonWebsocketConsumer
from channels import Channel, Group
import json

from radio.methods.playlist import get_current_track_info, get_playlist_stats_from_cache
from radio.methods.hosts import get_unique_listeners, add_unique_listener


from .client import dispatch

class WSConsumer(JsonWebsocketConsumer):

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["listener-%s" % self.path[1:]]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        Group("radio-listeners").add(message.reply_channel)
        message.reply_channel.send({"accept": True})

        # immidiately send events for song status
        track_name, track_author, track_comment = get_current_track_info()
        events = [
        {
            'type': 'CHANGE_TRACK_NAME',
            'name': track_name,
            'author': track_author
        },
        {
            'type': 'CHANGE_TRACK_COMMENT',
            'comment': track_comment
        }]
        for event in events:
            message.reply_channel.send({
                'text': json.dumps(event)
            })

        #update unique listeners
        host = dict(message.content['headers']).get(b'x-real-ip', b'0.0.0.0').decode()
        add_unique_listener(host)
        count = get_unique_listeners()
        action = {
            'type': 'SET_UNIQUE_LISTENERS',
            'count': count
        }
        Channel('radio-events').send(action)

        #update playlist stats
        query_size, unique_senders = get_playlist_stats_from_cache()
        actions = [{
            'type': 'SET_QUERY_SIZE',
            'size': query_size
        },{
            'type': 'SET_UNIQUE_SENDERS',
            'count': unique_senders
        }]
        for action in actions:
            message.reply_channel.send({
                'text': json.dumps(action)
            })

    def receive(self, content, **kwargs):
        """
        Called when a message is received with decoded JSON content
        """
        print(content)
        dispatch(content, self.path[1:])

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass


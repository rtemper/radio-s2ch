from channels import Channel, Group
from channels.sessions import channel_session
import json

from .methods.playlist import get_current_track_info, get_playlist_stats_from_cache
from .methods.hosts import get_unique_listeners, add_unique_listener


# Connected to radio-events
def msg_consumer(message):
    Group("radio-listeners").send({
        "text": json.dumps(message.content)
    })


@channel_session
def ws_connect(message):
    uuid = message.content['path'][1:]
    Group("listener-%s" % uuid).add(message.reply_channel)
    message.reply_channel.send({"accept": True})
    message.reply_channel.send({
        'text': "You subscribed to group %s" % uuid
    })
    Group("listener-%s" % uuid).send({
        "text": "Test message from group %s" % uuid
    })


# Connected to websocket.connect
@channel_session
def ws_connect1(message):
    # Save room in session and add us to the group
    # message.channel_session['room'] = room

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



# Connected to websocket.receive
@channel_session
def ws_message(message):
    msg = json.loads(message['text'])
    print(msg)
    Channel("radio-events").send({
        "type": msg['type'],
        "payload": msg['payload']
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("radio-listeners").discard(message.reply_channel)



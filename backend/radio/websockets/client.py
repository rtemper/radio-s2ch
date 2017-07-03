from channels import Group
import json

def ReplyToUUID(content, uuid):
    Group("listener-%s" % uuid).send({
        'text': json.dumps(content)
    })

def TrackLiked(msg, uuid):
    # Group("listener-%s" % uuid).send({
    #     'text': "Track liked by %s" % uuid
    # })
    ReplyToUUID({
        'type': 'LIKE_RECEIVED',
    }, uuid)
    print("Track liked from %s" % uuid )

def TrackCommented(msg, uuid):
    pass

handlers = {
    'TRACK_LIKED': TrackLiked,
    'TRACK_COMMENTED': TrackCommented,
}

import pdb
def dispatch(msg, uuid):
    action = msg.get('action', None)
    if not action:
        return
    handler = handlers.get(action, None)
    if not handler:
        return
    handler(msg, uuid)

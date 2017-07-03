from channels.routing import route, route_class
from radio.consumers import ws_connect, ws_disconnect, ws_message, msg_consumer

from radio.websockets.main import WSConsumer
from radio.websockets import client

channel_routing = [
    # route('websocket.connect', ws_connect),
    # route('websocket.receive', ws_message),
    # route('websocket.disconnect', ws_disconnect),
    route_class(WSConsumer),
    route('radio-events', msg_consumer)
]

import socketio
from urllib.parse import parse_qs
import json

sio = socketio.Server(cors_allowed_origins='*')


@sio.event
def connect(sid, environ):
    network_id = parse_qs(environ.get('QUERY_STRING')).get('network_id', [None])[0]
    if network_id:
        sio.enter_room(sid, network_id)


@sio.event
def send_packet(sid, message):
    data = json.loads(message)
    if (packet := data.get('packet')) and (network_id := data.get('network_id')):
        sio.emit('send_packet', packet, room=network_id)

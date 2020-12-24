import socketio
from urllib.parse import parse_qs
import json

sio = socketio.Server(cors_allowed_origins='*')

networks = {}


@sio.event
def connect(sid, environ):
    network_id = parse_qs(environ.get('QUERY_STRING')).get('network_id', [None])[0]
    is_forwarder = parse_qs(environ.get('QUERY_STRING')).get('is_forwarder', [None])[0]
    if network_id:
        sio.enter_room(sid, network_id)
        if is_forwarder:
            if not networks.get(network_id):
                networks[network_id] = [sid]
            else:
                networks[network_id].append(sid)
            notice = {
                'text': 'Packet forwarder has started.',
                'type': 'success'
            }
            sio.emit('notice', notice, room=network_id)


@sio.event
def disconnect(sid):
    rooms = sio.rooms(sid)
    rooms.remove(sid)
    network_id = rooms[0]
    networks[network_id].remove(sid)
    notice = {
        'text': 'Packet forwarder has stopped.',
        'type': 'error'
    }
    sio.emit('notice', notice, room=network_id)


@sio.event
def send_packet(sid, message):
    data = json.loads(message)
    if (packet := data.get('packet')) and (network_id := data.get('network_id')):
        sio.emit('send_packet', packet, room=network_id)

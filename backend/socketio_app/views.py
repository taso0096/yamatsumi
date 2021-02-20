from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from networks.models import Network
from exercises.models import Exercise

import socketio
from urllib.parse import parse_qs
import json

sio = socketio.Server(cors_allowed_origins='*')

networks = {}


class AnswerView(GenericAPIView):
    def post(self, request, network_id):
        try:
            network = Network.objects.get(network_id=network_id)
            Exercise.objects.get(network=network)
            response_data = {
                "uid": request.data['uid'],
                "qid": request.data['qid'],
                "isCorrect": request.data['isCorrect']
            }
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sio.emit('answer', response_data, room=network_id)
        return Response(status=status.HTTP_200_OK)


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
def packet(sid, data):
    loads_data = json.loads(data)
    if (packet := loads_data.get('packet')) and (network_id := loads_data.get('network_id')):
        sio.emit('packet', packet, room=network_id)

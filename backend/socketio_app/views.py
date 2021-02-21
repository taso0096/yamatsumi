from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from exercises.models import Exercise

import socketio
from urllib.parse import parse_qs
import json

sio = socketio.Server(cors_allowed_origins='*')

networks = {}


class AnswerView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, exercise_id):
        try:
            Exercise.objects.get(exercise_id=exercise_id)
            response_data = {
                "uid": request.data['uid'],
                "qid": request.data['qid'],
                "isCorrect": request.data['isCorrect']
            }
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sio.emit('answer', response_data, room=exercise_id)
        return Response(status=status.HTTP_200_OK)


@sio.event
def connect(sid, environ):
    exercise_id = parse_qs(environ.get('QUERY_STRING')).get('exercise_id', [None])[0]
    is_forwarder = parse_qs(environ.get('QUERY_STRING')).get('is_forwarder', [None])[0]
    if exercise_id:
        sio.enter_room(sid, exercise_id)
        if is_forwarder:
            if not networks.get(exercise_id):
                networks[exercise_id] = [sid]
            else:
                networks[exercise_id].append(sid)
            notice = {
                'text': 'Packet forwarder has started.',
                'type': 'success'
            }
            sio.emit('notice', notice, room=exercise_id)


@sio.event
def disconnect(sid):
    rooms = sio.rooms(sid)
    rooms.remove(sid)
    exercise_id = rooms[0]
    networks[exercise_id].remove(sid)
    notice = {
        'text': 'Packet forwarder has stopped.',
        'type': 'error'
    }
    sio.emit('notice', notice, room=exercise_id)


@sio.event
def packet(sid, data):
    loads_data = json.loads(data)
    if (packet := loads_data.get('packet')) and (exercise_id := loads_data.get('exercise_id')):
        sio.emit('packet', packet, room=exercise_id)

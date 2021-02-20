from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from exercises.models import Exercise
from .models import Network

import json
import uuid


def return_network_detail_data(network):
    data = {
        'id': network.network_id,
        'label': network.label,
        'desc': network.desc,
        'version': network.version,
        'routingTable': network.routing_table,
        'layers': network.layers
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'networkId': network.network_id,
        'username': network.user.username,
        'data': data,
        'createdAt': network.created_at,
        'updatedAt': network.updated_at
    }
    return response_data


class NetworksView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        try:
            if not (exercise := Exercise.objects.get(exercise_id=loads_data['id'])) or Network.objects.get(exercise=exercise):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            pass
        network_data = {
            'exercise': exercise,
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        try:
            network = Network.objects.create(**network_data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=return_network_detail_data(network), status=status.HTTP_201_CREATED)


class NetworkDetailView(GenericAPIView):
    def get(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        network = Network.objects.get(exercise=exercise)
        return Response(data=return_network_detail_data(network), status=status.HTTP_200_OK)

    def put(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        network = Network.objects.get(exercise=exercise)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        network_data = {
            'exercise': exercise,
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        for key, value in network_data.items():
            setattr(exercise, key, value)
        network.save()
        return Response(data=return_network_detail_data(exercise), status=status.HTTP_200_OK)

    def delete(self, request, exercise_id):
        exercese = Exercise.objects.get(exercise_id=exercise_id)
        Network.objects.filter(exercese=exercese).delete()
        return Response(status=status.HTTP_200_OK)

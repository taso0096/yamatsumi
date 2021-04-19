from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from exercises.models import Exercise
from .models import Cyberspace

import json


def return_cyberspace_detail_data(cyberspace):
    data = {
        'id': cyberspace.exercise.exercise_id,
        'version': cyberspace.version,
        'routingTable': cyberspace.routing_table,
        'layers': cyberspace.layers
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'exercise_id': cyberspace.exercise.exercise_id,
        'data': data,
        'createdAt': cyberspace.created_at,
        'updatedAt': cyberspace.updated_at
    }
    return response_data


class CyberspacesView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        try:
            if not (exercise := Exercise.objects.get(exercise_id=loads_data['id'])) or Cyberspace.objects.get(exercise=exercise):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            pass
        cyberspace_data = {
            'exercise': exercise,
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        try:
            cyberspace = Cyberspace.objects.create(**cyberspace_data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=return_cyberspace_detail_data(cyberspace), status=status.HTTP_201_CREATED)


class CyberspaceDetailView(GenericAPIView):
    def get(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        cyberspace = Cyberspace.objects.get(exercise=exercise)
        return Response(data=return_cyberspace_detail_data(cyberspace), status=status.HTTP_200_OK)

    def put(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        try:
            cyberspace = Cyberspace.objects.get(exercise=exercise)
        except Exception:
            cyberspace = None
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        cyberspace_data = {
            'exercise': exercise,
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        if cyberspace:
            for key, value in cyberspace_data.items():
                setattr(cyberspace, key, value)
            cyberspace.save()
        else:
            cyberspace = Cyberspace.objects.create(**cyberspace_data)
        return Response(data=return_cyberspace_detail_data(cyberspace), status=status.HTTP_200_OK)

    def delete(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        Cyberspace.objects.filter(exercise=exercise).delete()
        return Response(status=status.HTTP_200_OK)

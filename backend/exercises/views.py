from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from networks.models import Network
from .models import Exercise

import json


def return_exercise_data(exercise):
    data = {
        'id': exercise.network.network_id,
        'version': exercise.version,
        'teams': exercise.teams,
        'users': exercise.users,
        'levels': exercise.levels,
        'categories': exercise.categories,
        'questions': exercise.questions,
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'data': data,
        'createdAt': exercise.created_at,
        'updatedAt': exercise.updated_at
    }
    return response_data


class ExercisesView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        try:
            if not (network := Network.objects.get(network_id=loads_data['id'])) or Exercise.objects.get(network=network):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            pass
        exercise_data = {
            'network': network,
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        try:
            exercise = Exercise.objects.create(**exercise_data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=return_exercise_data(exercise), status=status.HTTP_201_CREATED)


class ExerciseDetailView(GenericAPIView):
    def get(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        exercise = Exercise.objects.get(network=network)
        return Response(data=return_exercise_data(exercise), status=status.HTTP_200_OK)

    def put(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        exercise = Exercise.objects.get(network=network)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        exercise_data = {
            'network': network,
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        for key, value in exercise_data.items():
            setattr(exercise, key, value)
        exercise.save()
        return Response(data=return_exercise_data(exercise), status=status.HTTP_200_OK)

    def delete(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        Exercise.objects.filter(network=network).delete()
        return Response(status=status.HTTP_200_OK)

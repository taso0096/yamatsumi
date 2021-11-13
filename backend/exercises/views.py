from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from cyberspaces.models import Cyberspace
from .models import Exercise

import json
import requests

def return_exercise_detail_data(exercise):
    data = {
        'id': exercise.cyberspace.cyberspace_id,
        'scoreUrl': exercise.score_url,
        'version': exercise.version,
        'teams': exercise.teams,
        'users': exercise.users,
        'levels': exercise.levels,
        'categories': exercise.categories,
        'questions': exercise.questions,
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'id': exercise.cyberspace.cyberspace_id,
        'username': exercise.cyberspace.user.username,
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
            if not (cyberspace := Cyberspace.objects.get(cyberspace_id=loads_data['id'])) or Exercise.objects.get(cyberspace=cyberspace):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            pass
        exercise_data = {
            'cyberspace': cyberspace,
            'score_url': loads_data.get('scoreUrl'),
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
        return Response(data=return_exercise_detail_data(exercise), status=status.HTTP_201_CREATED)


class ExerciseDetailView(GenericAPIView):
    def get(self, _, cyberspace_id):
        cyberspace = Cyberspace.objects.get(cyberspace_id=cyberspace_id)
        score_data = {}
        questions_data = {}
        if cyberspace.scores_url:
            res = requests.get(cyberspace.scores_url)
            score_data = res.json()
        if cyberspace.questions_url:
            res = requests.get(cyberspace.questions_url)
            questions_data = res.json()
        if cyberspace.user_routing_url:
            res = requests.get(cyberspace.user_routing_url)
            user_routing_data = res.json()
        res = {
            'id': cyberspace_id,
            'scores': score_data,
            **questions_data,
            'routingTable': user_routing_data
        }
        return Response(data=res, status=status.HTTP_200_OK)

    def put(self, request, cyberspace_id):
        cyberspace = Cyberspace.objects.get(cyberspace_id=cyberspace_id)
        try:
            exercise = Exercise.objects.get(cyberspace=cyberspace)
        except Exception:
            exercise = None
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        exercise_data = {
            'cyberspace': cyberspace,
            'score_url': loads_data.get('scoreUrl'),
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        if exercise:
            for key, value in exercise_data.items():
                setattr(exercise, key, value)
            exercise.save()
        else:
            exercise = Exercise.objects.create(**exercise_data)
        return Response(data=return_exercise_detail_data(exercise), status=status.HTTP_200_OK)

    def delete(self, request, cyberspace_id):
        cyberspace = Cyberspace.objects.get(cyberspace_id=cyberspace_id)
        Exercise.objects.filter(cyberspace=cyberspace).delete()
        return Response(status=status.HTTP_200_OK)

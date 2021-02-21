from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Exercise

import json
import uuid


def return_exercise_data(exercise):
    response_data = {
        'exerciseId': exercise.exercise_id,
        'label': exercise.label,
        'username': exercise.user.username,
        'createdAt': exercise.created_at,
        'updatedAt': exercise.updated_at
    }
    return response_data


def return_exercise_detail_data(exercise):
    data = {
        'id': exercise.exercise_id,
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
    def get(self, request, *args, **kwargs):
        search_word = request.GET.get('search')
        exercises = Exercise.objects.all() if not search_word else Exercise.objects.filter(
            Q(exercise_id__icontains=search_word) | Q(label__icontains=search_word)
        )
        reponse_data = []
        for exercise in exercises:
            reponse_data.insert(0, return_exercise_data(exercise))
        return Response(data=reponse_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        exercise_data = {
            'exercise_id': loads_data.get('id') or uuid.uuid4(),
            'user': request.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
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
    def get(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        return Response(data=return_exercise_detail_data(exercise), status=status.HTTP_200_OK)

    def put(self, request, exercise_id):
        exercise = Exercise.objects.get(exercise_id=exercise_id)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        exercise_data = {
            'exercise_id': loads_data['id'],
            'user': exercise.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
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
        return Response(data=return_exercise_detail_data(exercise), status=status.HTTP_200_OK)

    def delete(self, request, exercise_id):
        Exercise.objects.filter(exercise_id=exercise_id).delete()
        return Response(status=status.HTTP_200_OK)

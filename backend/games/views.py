from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from networks.models import Network
from .models import Game

import json


def return_game_data(game):
    data = {
        'id': game.network.network_id,
        'version': game.version,
        'teams': game.teams,
        'users': game.users,
        'levels': game.levels,
        'categories': game.categories,
        'questions': game.questions,
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'data': data,
        'createdAt': game.created_at,
        'updatedAt': game.updated_at
    }
    return response_data


class GamesView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        try:
            if not (network := Network.objects.get(network_id=loads_data['id'])) or Game.objects.get(network=network):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            pass
        game_data = {
            'network': network,
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        try:
            game = Game.objects.create(**game_data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=return_game_data(game), status=status.HTTP_201_CREATED)


class GameDetailView(GenericAPIView):
    def get(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        game = Game.objects.get(network=network)
        return Response(data=return_game_data(game), status=status.HTTP_200_OK)

    def put(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        game = Game.objects.get(network=network)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        game_data = {
            'network': network,
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        for key, value in game_data.items():
            setattr(game, key, value)
        game.save()
        return Response(data=return_game_data(game), status=status.HTTP_200_OK)

    def delete(self, request, network_id):
        network = Network.objects.get(network_id=network_id)
        Game.objects.filter(network=network).delete()
        return Response(status=status.HTTP_200_OK)

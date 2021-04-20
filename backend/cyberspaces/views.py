from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Cyberspace

import json
import uuid


def return_cyberspace_data(cyberspace):
    response_data = {
        'id': cyberspace.cyberspace_id,
        'label': cyberspace.label,
        'username': cyberspace.user.username,
        'createdAt': cyberspace.created_at,
        'updatedAt': cyberspace.updated_at
    }
    return response_data


def return_cyberspace_detail_data(cyberspace):
    data = {
        'id': cyberspace.cyberspace_id,
        'label': cyberspace.label,
        'desc': cyberspace.desc,
        'version': cyberspace.version,
        'routingTable': cyberspace.routing_table,
        'layers': cyberspace.layers
    }
    data = {k: data[k] for k in data if data[k] is not None}
    response_data = {
        'id': cyberspace.cyberspace_id,
        'username': cyberspace.user.username,
        'data': data,
        'createdAt': cyberspace.created_at,
        'updatedAt': cyberspace.updated_at
    }
    return response_data


class CyberspacesView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        search_word = request.GET.get('search')
        cyberspaces = Cyberspace.objects.all() if not search_word else Cyberspace.objects.filter(
            Q(cyberspace_id__icontains=search_word) | Q(label__icontains=search_word)
        )
        reponse_data = []
        for cyberspace in cyberspaces:
            reponse_data.insert(0, return_cyberspace_data(cyberspace))
        return Response(data=reponse_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        cyberspace_data = {
            'cyberspace_id': loads_data.get('id') or uuid.uuid4(),
            'user': request.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
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
    def get(self, request, cyberspace_id):
        cyberspace = Cyberspace.objects.get(cyberspace_id=cyberspace_id)
        return Response(data=return_cyberspace_detail_data(cyberspace), status=status.HTTP_200_OK)

    def put(self, request, cyberspace_id):
        cyberspace = Cyberspace.objects.get(cyberspace_id=cyberspace_id)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        cyberspace_data = {
            'cyberspace_id': loads_data['id'],
            'user': cyberspace.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
            'score_url': loads_data.get('scoreUrl'),
            'version': loads_data.get('version'),
            'teams': loads_data.get('teams'),
            'users': loads_data.get('users'),
            'levels': loads_data.get('levels'),
            'categories': loads_data.get('categories'),
            'questions': loads_data.get('questions')
        }
        for key, value in cyberspace_data.items():
            setattr(cyberspace, key, value)
        cyberspace.save()
        return Response(data=return_cyberspace_detail_data(cyberspace), status=status.HTTP_200_OK)

    def delete(self, request, cyberspace_id):
        Cyberspace.objects.filter(cyberspace_id=cyberspace_id).delete()
        return Response(status=status.HTTP_200_OK)

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Network

import json
import uuid


def return_network_data(network):
    response_data = {
        'networkId': network.network_id,
        'label': network.label,
        'username': network.user.username,
        'layerCount': len(network.layers),
        'nodeCount': len(network.routing_table or {}),
        'createdAt': network.created_at,
        'updatedAt': network.updated_at
    }
    return response_data


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
    def get(self, request, *args, **kwargs):
        search_word = request.GET.get('search')
        networks = Network.objects.all() if not search_word else Network.objects.filter(
            Q(network_id__icontains=search_word) | Q(label__icontains=search_word)
        )
        reponse_data = []
        for network in networks:
            reponse_data.insert(0, return_network_data(network))
        return Response(data=reponse_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        network_data = {
            'network_id': loads_data.get('id') or uuid.uuid4(),
            'user': request.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        try:
            network = Network.objects.create(**network_data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=return_network_data(network), status=status.HTTP_201_CREATED)


class NetworkDetailView(GenericAPIView):
    def get(self, request, network_id):
        network = Network.objects.get(pk=network_id)
        return Response(data=return_network_detail_data(network), status=status.HTTP_200_OK)

    def put(self, request, network_id):
        network = Network.objects.get(pk=network_id)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            loads_data = json.loads(data)
        except Exception:
            loads_data = data
        network_data = {
            'network_id': loads_data['id'],
            'user': network.user,
            'label': loads_data.get('label'),
            'desc': loads_data.get('desc'),
            'version': loads_data.get('version'),
            'routing_table': loads_data.get('routingTable'),
            'layers': loads_data['layers']
        }
        if network_id == loads_data['id']:
            for key, value in network_data.items():
                setattr(network, key, value)
            network.save()
        else:
            network.delete()
            network = Network.objects.create(**network_data)
        return Response(data=return_network_detail_data(network), status=status.HTTP_200_OK)

    def delete(self, request, network_id):
        Network.objects.filter(pk=network_id).delete()
        return Response(status=status.HTTP_200_OK)

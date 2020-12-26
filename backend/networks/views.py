from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Network

import json


def return_network_data(network):
    response_data = {
        'networkId': network.network_id,
        'username': network.user.username,
        'data': network.data,
        'createdAt': network.created_at,
        'updatedAt': network.updated_at
    }
    return response_data


class NetworksView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        networks = Network.objects.all()
        reponse_data = []
        for network in networks:
            reponse_data.append(return_network_data(network))
        return Response(data=reponse_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        loads_data = json.loads(data)
        network_data = {
            'network_id': loads_data['id'],
            'user': request.user,
            'data': loads_data
        }
        network = Network.objects.create(**network_data)
        return Response(data=return_network_data(network), status=status.HTTP_201_CREATED)


class NetworkDetailView(GenericAPIView):
    def get(self, request, network_id):
        network = Network.objects.get(pk=network_id)
        return Response(data=return_network_data(network), status=status.HTTP_200_OK)

    def put(self, request, network_id):
        network = Network.objects.get(pk=network_id)
        if not (data := request.data['data']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        loads_data = json.loads(data)
        if network_id == loads_data['id']:
            network.data = loads_data
            network.save()
        else:
            network_data = {
                'network_id': loads_data['id'],
                'user': network.user,
                'data': loads_data
            }
            network.delete()
            network = Network.objects.create(**network_data)
        return Response(data=return_network_data(network), status=status.HTTP_200_OK)

    def delete(self, request, network_id):
        Network.objects.filter(pk=network_id).delete()
        return Response(status=status.HTTP_200_OK)

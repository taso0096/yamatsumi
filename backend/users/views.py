from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


def return_user_data(user):
    response_data = {
        'username': user.username,
        'isSuperuser': user.is_superuser,
    }
    return response_data


class IsAuthenticatedOrPost(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user = request.user
        return user.is_active


class GetMyDataView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(data=return_user_data(request.user), status=status.HTTP_200_OK)


class UsersView(GenericAPIView):
    permission_classes = (IsAuthenticatedOrPost,)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        reponse_data = []
        for user in users:
            reponse_data.append(return_user_data(user))
        return Response(data=reponse_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not ((username := request.data['username']) and (password := request.data['password'])):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = ({
            'username': username,
            'is_active': True,
            'is_superuser': True,
        })
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return Response(data=return_user_data(user), status=status.HTTP_201_CREATED)

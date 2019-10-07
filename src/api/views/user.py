from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import User
from api.serializers import UserCreationSerializer, UserSerializer
from api.services import UserService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # register
    def create(self, request, *args, **kwargs):
        data = UserService.get_creation_data(request.data.copy(), 'distributor')
        serializer = UserCreationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        payload = {
            "username": serializer.data['username'],
            "iat": datetime.now().timestamp()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        data = serializer.data.copy()
        data['result'] = token.decode("utf-8")
        data['success'] = True
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success': True,
                         'result': serializer.data})

    @action(methods=['put'], detail=True)
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.password = make_password(request.data.get('password'), salt=settings.SECRET_KEY)
        instance.save()
        return Response({"success": True})

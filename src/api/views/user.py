from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import User
from api.serializers import UserCreationSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # register
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['password'] = make_password(data.get('password'), salt=settings.SECRET_KEY)
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

    # get list user
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).exclude(role='mod')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    # get profile
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

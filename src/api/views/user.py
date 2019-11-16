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

    # get supplier profile
    @action(methods=['get'], detail=True)
    def retrieve_supplier(self, request, *args, **kwargs):
        supplier = User.objects.get(id=kwargs.get('pk'))
        serializer = self.get_serializer(supplier)
        return Response({'success': True,
                         'result': serializer.data})

    # update profile
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'success': True,
                         'result': serializer.data})

    # get list farmer
    @action(methods=['get'], detail=False)
    def list_farmer(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(role='farmer')

        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    @action(methods=['put'], detail=True)
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.password = make_password(request.data.get('password'), salt=settings.SECRET_KEY)
        instance.save()
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

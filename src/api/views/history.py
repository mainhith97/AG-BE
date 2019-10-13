from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import History, Cart
from api.serializers import HistorySerializer


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    # add to history
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Cart.objects.filter(user=request.data.get('user_id')).delete()
        self.perform_create(serializer)
        return Response({'success': True,
                         'result': serializer.data},
                        status=status.HTTP_201_CREATED)

    # get list history
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    # get list history by user
    def retrieve(self, request, *args, **kwargs):
        user_history = self.filter_queryset(self.get_queryset()).filter(user_id=kwargs.get('pk'))
        serializer = self.get_serializer(user_history, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    # change status
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
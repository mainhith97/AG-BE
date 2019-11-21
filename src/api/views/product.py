from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Product, User, Type
from api.serializers import ProductSerializer, UserSerializer, TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # get list product
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        datas = serializer.data.copy()
        user_query = User.objects.all()
        type_query = Type.objects.all()
        for data in datas:
            for i in user_query:
                if i.id == data.get('provider_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['provider'] = user_serializer.data
            for i in type_query:
                if i.id == data.get('type'):
                    typetype = i
                    type_serializer = TypeSerializer(typetype)
                    data['typetype'] = type_serializer.data
        return Response({'success': True,
                         'result': datas})

    # get detail product
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user = User.objects.get(id=serializer.data.get('provider_id'))
        user_serializer = UserSerializer(user)
        type = Type.objects.get(id=serializer.data.get('type'))
        type_serializer = TypeSerializer(type)
        return Response({'success': True,
                         'result': serializer.data,
                         'user': user_serializer.data,
                         'type': type_serializer.data})

    # get list newest
    @action(methods=['get'], detail=False)
    def get_list_newest(self, request, *args, **kwargs):
        products = Product.objects.order_by('-created_at')[:8]
        serializer = self.get_serializer(products, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by farmer
    # detail= True la co id
    @action(methods=['get'], detail=True)
    def list_by_farmer(self, request, *args, **kwargs):
        queryset = self.queryset.filter(provider_id=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)
        type_query = Type.objects.all()
        for data in serializer.data:
            for i in type_query:
                if i.id == data.get('type'):
                    typetype = i
                    type_serializer = TypeSerializer(typetype)
                    data['typetype'] = type_serializer.data
        return Response({'success': True,
                         'result': serializer.data})

    # create product
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    # edit product
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

        return Response({'success': True, 'result': serializer.data})

    # delete product
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

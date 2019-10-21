from rest_framework import viewsets
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
        return Response({'success': True,
                         'result': serializer.data,
                         'user': user_serializer.data})

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

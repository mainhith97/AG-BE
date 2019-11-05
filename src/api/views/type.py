from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Product, Type
from api.serializers import TypeSerializer, ProductSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    # get list category
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category
    def retrieve(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk'))
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category lastest
    @action(methods=['get'], detail=True)
    def retrieve_lastest(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk')).order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category price low to high
    @action(methods=['get'], detail=True)
    def retrieve_pricelow(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk')).order_by('price_per_unit')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category price high to low
    @action(methods=['get'], detail=True)
    def retrieve_pricehigh(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk')).order_by('-price_per_unit')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

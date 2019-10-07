from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Product, User
from api.serializers import ProductSerializer, UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

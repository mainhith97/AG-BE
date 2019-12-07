from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Product, Type, User
from api.serializers import TypeSerializer, ProductSerializer, UserSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.filter(active=True)
    serializer_class = TypeSerializer

    # get list category
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            product_query = Product.objects.filter(active=True, type=data.get('id'))
            data['product'] = product_query.count()
        return Response({'success': True,
                         'result': serializer.data})

    def create(self, request, *args, **kwargs):
        request.data['active'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        data['active'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'success': True, 'result': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        Product.objects.filter(type=instance.id).update(active=False)
        return Response(data={'success': True})

    # get list product by category oldest
    def retrieve(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk'), provider_id__active=True, active=True)
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        datas = serializer.data.copy()
        user_query = User.objects.filter(active=True)
        type_query = Type.objects.filter(active=True)
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

    # get type
    @action(methods=['get'], detail=True)
    def retrieve_type(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category lastest
    @action(methods=['get'], detail=True)
    def retrieve_lastest(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk'), provider_id__active=True, active=True).order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category price low to high
    @action(methods=['get'], detail=True)
    def retrieve_pricelow(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk'), provider_id__active=True, active=True).order_by('price_per_unit')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

    # get list product by category price high to low
    @action(methods=['get'], detail=True)
    def retrieve_pricehigh(self, request, *args, **kwargs):
        products = Product.objects.filter(type=kwargs.get('pk'), provider_id__active=True, active=True).order_by('-price_per_unit')
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            product['image'] = 'http://127.0.0.1:8001' + product['image']
        return Response({'success': True,
                         'result': serializer.data})

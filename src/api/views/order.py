from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Order, User, Product
from api.serializers import UserSerializer, ProductSerializer
from api.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('product_id')
    serializer_class = OrderSerializer

    # add to order
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    # get list order by distributor
    @action(methods=['get'], detail=True)
    def retrieve_by_distributor(self, request, *args, **kwargs):
        user_orders = self.filter_queryset(self.get_queryset()).filter(user_id=kwargs.get('pk'))
        serializer = self.get_serializer(user_orders, many=True)
        datas = serializer.data.copy()
        product_query = Product.objects.all()
        for data in datas:
            for i in product_query:
                if i.id == data.get('product_id'):
                    product_order = i
                    product_serializer = ProductSerializer(product_order)
                    data['product_order'] = product_serializer.data
        return Response({'success': True,
                         'result': datas})

    # get list order by farmer
    @action(methods=['get'], detail=True)
    def retrieve_by_farmer(self, request, *args, **kwargs):
        user_orders = self.filter_queryset(self.get_queryset()).filter(product_id__provider_id=kwargs.get('pk'))
        for order in user_orders:
            if order.status == 'Đang chờ':
                order.status = "Đã xem"
                order.save()
        serializer = self.get_serializer(user_orders, many=True)
        datas = serializer.data.copy()
        user_query = User.objects.all()
        product_query = Product.objects.all()
        for data in datas:
            for i in user_query:
                if i.id == data.get('user_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['user_order'] = user_serializer.data
            for i in product_query:
                if i.id == data.get('product_id'):
                    product_order = i
                    product_serializer = ProductSerializer(product_order)
                    data['product_order'] = product_serializer.data
        return Response({'success': True,
                         'result': datas})

    # unseen order
    @action(methods=['get'], detail=True)
    def get_unseen_orders(self, request, *args, **kwargs):
        unseen_orders = self.filter_queryset(self.get_queryset()).filter(product_id__provider_id=kwargs.get('pk'),
                                                                         status='Đang chờ').count()
        return Response({'success': True,
                         'result': unseen_orders})

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

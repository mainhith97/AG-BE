from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Product, Waitinglist
from api.serializers import ProductSerializer, WaitinglistSerializer


class WaitinglistViewSet(viewsets.ModelViewSet):
    queryset = Waitinglist.objects.all()
    serializer_class = WaitinglistSerializer

    # add to waiting list
    def create(self, request, *args, **kwargs):
        if Waitinglist.objects.filter(user=request.data.get('user'), product=request.data.get('product')).count():
            raise ValidationError('Product already existed in waiting list.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': True})

    # get list order by distributor
    @action(methods=['get'], detail=True)
    def retrieve_by_distributor(self, request, *args, **kwargs):
        user_orders = self.filter_queryset(self.get_queryset()).filter(user=kwargs.get('pk'))
        serializer = self.get_serializer(user_orders, many=True)
        datas = serializer.data.copy()
        product_query = Product.objects.select_related('provider_id')
        for data in datas:
            for i in product_query:
                if i.id == data.get('product'):
                    product_order = i
                    product_serializer = ProductSerializer(product_order)
                    data['provider'] = i.provider_id.company_name
                    product_data = product_serializer.data.copy()
                    product_data['image'] = 'http://127.0.0.1:8001' + str(product_data['image'])
                    data['product_order'] = product_data
        return Response({'success': True, 'result': datas})

    # delete waiting list
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import History, Cart, Product
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
        for data in serializer.data:
            products = data.get('products').split('\n')
            product_list = []
            for product in products:
                quantity = int(product.split()[0])
                unit = product.split()[1]
                name = ' '.join(product.split()[2:])
                product_detail = Product.objects.select_related('provider_id').get(name=name)
                provider = product_detail.provider_id.company_name
                total = quantity * int(product_detail.price_per_unit)
                product_list.append({'name': name,
                                     'quantity': str(quantity) + ' ' + unit,
                                     'provider': provider,
                                     'total': total})
            data['products'] = product_list
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

    # get list history by farmer
    @action(methods=['get'], detail=True)
    def list_by_farmer(self, request, *args, **kwargs):
        product_list = []
        sum_total = 0
        histories = self.filter_queryset(self.get_queryset()).values('name', 'products', 'status')
        for history in histories:
            products = history.get('products').split('\n')
            for product in products:
                name = ' '.join(product.split()[2:])
                product_detail = Product.objects.select_related('provider_id').get(name=name)
                if product_detail.provider_id_id == int(kwargs.get('pk')):
                    quantity = int(product.split()[0])
                    unit = product.split()[1]
                    provider = product_detail.provider_id.company_name
                    total = quantity * int(product_detail.price_per_unit)
                    sum_total = sum_total + total
                    product_list.append({'buyer': history.get('name'),
                                         'product_name': name,
                                         'quantity': str(quantity) + ' ' + unit,
                                         'provider': provider,
                                         'total': total,
                                         'status': history.get('status')
                                         })
        return Response({'success': True,
                         'sum_total': sum_total,
                         'result': product_list})

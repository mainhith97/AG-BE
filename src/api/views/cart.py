from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Cart, Product
from api.serializers import CartSerializer, ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    # add to cart
    def create(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset()).filter(product=request.data.get('product'), user=request.data.get('user'))
        if query.count():
            product = query.first()
            product.quantity = product.quantity + 1
            product.save()
        else:
            data = request.data.copy()
            data['quantity'] = 1
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({'success': True})

    # get cart and calculate total price
    def retrieve(self, request, *args, **kwargs):
        kwargs_id = kwargs.get('pk')
        queryset = self.get_queryset().filter(user=kwargs_id)
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            product_value = Product.objects.get(id=data.get('product'))
            product_serializer = ProductSerializer(product_value)
            product_data = product_serializer.data.copy()
            product_data['image'] = 'http://127.0.0.1:8001' + product_data['image']
            data['product_value'] = product_data
            data['total'] = data.get('quantity') * product_data.get('price_per_unit')
        return Response({'success': True,
                         'result': serializer.data,
                         'totals': sum(i.get('total') for i in serializer.data)})

    # update cart
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

    # delete cart
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Product, User, Cart, History, Order, Comment, Type
from api.serializers import ProductSerializer, UserSerializer, TypeSerializer
from api.services.token import Token


class ActionViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # login
    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = make_password(password=request.data.get('password'), salt=settings.SECRET_KEY)
        try:
            user = User.objects.get(username=username,
                                    password=password)
            token = Token.encode(user)
            carts = Cart.objects.filter(user=user.id).values("quantity")
            cart_count = sum(cart.get('quantity') for cart in carts)
        except ValueError:
            raise ValidationError("Invalid username or password")
        return Response({"success": True,
                         "result": token,
                         "id": user.id,
                         "username": username,
                         "role": user.role,
                         "cart": cart_count})

    # search
    @action(methods=['post'], detail=False)
    def search(self, request, *args, **kwargs):
        return Response({"success": True,
                         "result": request.data.get('keyword')})

    # get search result
    @action(methods=['get'], detail=False)
    def get_search_result(self, request, *args, **kwargs):
        try:
            products = Product.objects.filter(name__icontains=request.query_params.get('keyword'))
            product_serializer = ProductSerializer(products, many=True)
            for product in product_serializer.data:
                product['image'] = 'http://127.0.0.1:8001' + product['image']
            datas = product_serializer.data.copy()
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
            return Response({"success": True,
                             "result": datas})
        except ValueError:
            return Response({'success': False,
                             'result': None})

    # statistic
    @action(methods=['get'], detail=False)
    def get_statistic(self, request, *args, **kwargs):
        user_query = User.objects.exclude(role='mod')
        farmers = user_query.filter(role='farmer').count()
        distributors = user_query.filter(role='distributor').count()
        products = Product.objects.all().count()
        sales = History.objects.all().count()
        requests = Order.objects.all().count()
        return Response({"success": True,
                         "users": {'users': user_query.count(), 'farmers': farmers, 'distributors': distributors},
                         "products": products,
                         "sales": sales,
                         "requests": requests})

    # statistic by farmer
    @action(methods=['get'], detail=True)
    def get_statistic_by_farmer(self, request, *args, **kwargs):
        product_history = Product.objects.filter(provider_id=kwargs.get('pk'))

        product_list = 0
        sum_total = 0
        histories = History.objects.all().values('name', 'products', 'status')
        for history in histories:
            products = history.get('products').split('\n')
            for product in products:
                name = ' '.join(product.split()[2:])
                product_detail = Product.objects.select_related('provider_id').get(name=name)
                if product_detail.provider_id_id == int(kwargs.get('pk')):
                    quantity = int(product.split()[0])
                    total = quantity * int(product_detail.price_per_unit)
                    sum_total = sum_total + total
                    product_list += 1

        orders = Order.objects.select_related('product_id').filter(product_id__provider_id=kwargs.get('pk'))
        accepted_orders = orders.filter(status='Chấp nhận')
        accepted_orders_revenue = sum(order.proposed_price for order in accepted_orders)

        responses = Comment.objects.select_related('product_id').filter(
            product_id__provider_id=kwargs.get('pk')).count()
        return Response({"success": True,
                         "products": product_history.count(),
                         'history': {
                             'count': product_list,
                             'revenue': sum_total
                         },
                         "orders": {
                             'total': orders.count(),
                             'accepted': accepted_orders.count(),
                             'revenue': accepted_orders_revenue
                         },
                         'total_revenue': sum_total+accepted_orders_revenue,
                         "responses": responses})

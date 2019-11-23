import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Product, User, Cart, History, Order, Comment, Type
from api.serializers import ProductSerializer, UserSerializer, TypeSerializer, ProductPopular
from api.services.email import EmailThread
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
                                    password=password,
                                    active=True)
            token = Token.encode(user)
            carts = Cart.objects.filter(user=user.id).values("quantity")
            cart_count = sum(cart.get('quantity') for cart in carts)
        except:
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
            products = Product.objects.filter(name__icontains=request.query_params.get('keyword'),
                                              provider_id__active=True)
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

    # admin search user
    @action(methods=['get'], detail=False)
    def get_search_user(self, request, *args, **kwargs):
        try:
            users = User.objects.filter(company_name__icontains=request.query_params.get('keyword'), active=True)
            user_serializer = UserSerializer(users, many=True)
            return Response({"success": True,
                             "result": user_serializer.data})
        except ValueError:
            return Response({'success': False,
                             'result': None})

    # statistic
    @action(methods=['get'], detail=False)
    def get_statistic(self, request, *args, **kwargs):
        user_query = User.objects.exclude(role='mod')
        farmers = user_query.filter(role='farmer').count()
        distributors = user_query.filter(role='distributor').count()
        banned_users = user_query.filter(active=False).count()
        products = Product.objects.all().count()
        sales = History.objects.all().count()
        requests = Order.objects.all().count()
        return Response({"success": True,
                         "users": {'users': user_query.count(), 'farmers': farmers, 'distributors': distributors, 'banned_users': banned_users},
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
        accepted_orders = orders.filter(status='Accept')
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
                         'total_revenue': sum_total + accepted_orders_revenue,
                         "responses": responses})

    @action(methods=['post'], detail=False)
    def forgot_password(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            token = Token.encode(user)
            link = f'http://localhost:4200/change_password?token={token}'
        except:
            raise Exception('User does not exist')

        content = render_to_string('../templates/email.html', {'link': link})

        EmailThread(subject='Forgot Password', email=[request.data.get('email')], content=content).start()
        return Response({"success": True})

    @action(methods=['post'], detail=False)
    def change_password(self, request, *args, **kwargs):
        user = Token.decode(request.data.get('token'))
        user.password = make_password(request.data.get('password'), salt=settings.SECRET_KEY)
        user.save()
        return Response({"success": True})

    @action(methods=['get'], detail=False)
    def get_list_popular(self, request, *args, **kwargs):
        day = datetime.datetime.now()
        products = Product.objects.filter(provider_id__active=True)
        serializer = ProductPopular(products, many=True)
        for data in serializer.data:
            history_count = 0
            history = History.objects.filter(created_at__month=day.month)
            data['image'] = 'http://127.0.0.1:8001' + data['image']
            for i in history:
                products_name = [' '.join(j.split()[2:]) for j in i.products.split('\n')]
                products = [product.id for product in Product.objects.filter(name__in=products_name)]
                if data.get('id') in products:
                    history_count += 5
            order = Order.objects.filter(product_id=data.get('id'), created_at__month=day.month).count() * 3
            comment = Comment.objects.filter(product_id=data.get('id'), created_at__month=day.month).count() * 2
            data['count'] = history_count + order + comment
        return Response({'success': True,
                         'result': serializer.data})

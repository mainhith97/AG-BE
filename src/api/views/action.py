from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Product, User, Cart
from api.serializers import ProductSerializer, UserSerializer
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
            return Response({"success": True,
                             "result": product_serializer.data})
        except ValueError:
            return Response({'success': False,
                             'result': None})

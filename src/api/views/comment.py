from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Comment, User, Product, Reply
from api.serializers import CommentSerializer, UserSerializer, ProductSerializer, ReplySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('product_id')
    serializer_class = CommentSerializer

    # post comment
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    # get a comment
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_query = User.objects.all()
        product_query = Product.objects.all()
        data = serializer.data.copy()
        data['created_at'] = data.get('created_at')[0:10]
        for i in user_query:
            if i.id == data.get('user_id'):
                user = i
                user_serializer = UserSerializer(user)
                data['user_cmt'] = user_serializer.data
        for i in product_query:
            if i.id == data.get('product_id'):
                product_order = i
                product_serializer = ProductSerializer(product_order)
                data['product_cmt'] = product_serializer.data
        return Response({'success': True,
                         'result': data})

    # get list comment by product
    @action(methods=['get'], detail=True)
    def retrieve_by_product(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(product_id=kwargs.get('pk')).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        reply_query = Reply.objects.all()
        user_query = User.objects.all()
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
            for i in user_query:
                if i.id == data.get('user_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['user_cmt'] = user_serializer.data
            replies = list(i for i in reply_query if i.cmt_id_id == data.get('id'))
            reply_serializer = ReplySerializer(replies, many=True)
            data['replies'] = len(replies)
        return Response({'success': True, 'result': serializer.data})

    # get list comment by admin
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
        datas = serializer.data.copy()
        user_query = User.objects.all()
        product_query = Product.objects.all()
        for data in datas:
            for i in user_query:
                if i.id == data.get('user_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['user_cmt'] = user_serializer.data
            for i in product_query:
                if i.id == data.get('product_id'):
                    product_order = i
                    product_serializer = ProductSerializer(product_order)
                    data['provider'] = i.provider_id.company_name
                    data['product_cmt'] = product_serializer.data
        return Response({'success': True,
                         'result': datas})

    # delete cmt
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

    # get list cmt by farmer
    @action(methods=['get'], detail=True)
    def retrieve_by_farmer(self, request, *args, **kwargs):
        user_cmt = self.filter_queryset(self.get_queryset()).filter(product_id__provider_id=kwargs.get('pk'))
        serializer = self.get_serializer(user_cmt, many=True)
        user_query = User.objects.all()
        product_query = Product.objects.all()
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
            for i in user_query:
                if i.id == data.get('user_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['user_cmt'] = user_serializer.data
            for i in product_query:
                if i.id == data.get('product_id'):
                    product_order = i
                    product_serializer = ProductSerializer(product_order)
                    data['product_cmt'] = product_serializer.data
        return Response({'success': True,
                         'result': serializer.data})



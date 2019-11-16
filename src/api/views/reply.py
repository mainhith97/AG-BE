from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Reply, User, Comment, Product
from api.serializers import ReplySerializer, UserSerializer, CommentSerializer, ProductSerializer


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    # post reply
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    # get list reply by farmer
    @action(methods=['get'], detail=True)
    def retrieve_by_farmer(self, request, *args, **kwargs):
        provider_reply = self.filter_queryset(self.get_queryset()).filter(provider_id=kwargs.get('pk'))
        serializer = self.get_serializer(provider_reply, many=True)
        comment_query = Comment.objects.all()
        product_query = Product.objects.all()
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
            for i in comment_query:
                if i.id == data.get('cmt_id'):
                    comment = i
                    comment_serializer = CommentSerializer(comment)
                    data['cmt'] = comment_serializer.data
                    for product in product_query:
                        if product.id == i.product_id_id:
                            product_order = product
                            product_serializer = ProductSerializer(product_order)
                            data['product_cmt'] = product_serializer.data
                continue
        return Response({'success': True,
                         'result': serializer.data})

    # delete reply
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True})

    # get list reply by comment
    @action(methods=['get'], detail=True)
    def retrieve_by_comment(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(cmt_id=kwargs.get('pk')).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
        datas = serializer.data.copy()
        user_query = User.objects.all()
        for data in datas:
            for i in user_query:
                if i.id == data.get('provider_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['provider_reply'] = user_serializer.data
        return Response({'success': True, 'result': datas})

    # get list reply by admin
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        comment_query = Comment.objects.all()
        product_query = Product.objects.all()
        user_query = User.objects.all()
        for data in serializer.data:
            data['created_at'] = data.get('created_at')[0:10]
            for i in comment_query:
                if i.id == data.get('cmt_id'):
                    comment = i
                    comment_serializer = CommentSerializer(comment)
                    data['cmt'] = comment_serializer.data
                    for product in product_query:
                        if product.id == i.product_id_id:
                            product_order = product
                            product_serializer = ProductSerializer(product_order)
                            data['product_cmt'] = product_serializer.data
                continue
            for i in user_query:
                if i.id == data.get('provider_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['provider_reply'] = user_serializer.data
        return Response({'success': True,
                         'result': serializer.data})
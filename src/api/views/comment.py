from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Comment, User
from api.serializers import CommentSerializer, UserSerializer


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

    # get list comment by product
    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(product_id=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)
        datas = serializer.data.copy()
        user_query = User.objects.all()
        for data in datas:
            for i in user_query:
                if i.id == data.get('user_id'):
                    user = i
                    user_serializer = UserSerializer(user)
                    data['user_cmt'] = user_serializer.data
        return Response({'success': True, 'result': datas})
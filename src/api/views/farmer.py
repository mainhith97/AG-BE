from rest_framework import status, viewsets
from rest_framework.response import Response

from api.models import User
from api.serializers import UserCreationSerializer, UserSerializer
from api.services import UserService


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = UserService.get_creation_data(request.data.copy(), 'farmer')
        serializer = UserCreationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

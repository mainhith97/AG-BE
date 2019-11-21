from rest_framework import status, viewsets
from rest_framework.response import Response

from api.models import Reason
from api.serializers import ReasonSerializer


class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

    # post reason
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'result': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

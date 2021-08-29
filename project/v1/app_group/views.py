from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from project.models import AppGroup
from .serializer import AppGroupSerializer


class AppGroupViewSet(viewsets.ModelViewSet):
    queryset = AppGroup.objects.all()
    serializer_class = AppGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(users__in=[self.request.user])

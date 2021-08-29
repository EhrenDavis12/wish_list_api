from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from project.models import WishList
from .serializer import WishListSerializer


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(owner=self.request.user)

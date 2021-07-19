# from rest_framework import status
# from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from project.models import WishList
from .serializer import WishListSerializer, WishListWriteSerializer


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(owner=self.request.user)

    def get_object(self, pk):
        wish_lists = self.get_queryset()
        wish_list = get_object_or_404(wish_lists, pk=pk)
        return wish_list

    def create(self, request, *args, **kwargs):
        serializer = WishListWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response({"status": True, "data": serializer.data})
        # return Response({"status": True, "pk": serializer.instance.pk})

    def list(self, request):
        wish_lists = self.get_queryset()
        serializer = self.get_serializer(wish_lists, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        wish_list = self.get_object(pk)
        serializer = self.get_serializer(wish_list)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        wish_list = self.get_object(pk)
        serializer = WishListWriteSerializer(
            wish_list, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "Error", "data": "invalid data"})

    def destroy(self, request, pk=None):
        wish_list = self.get_object(pk)
        wish_list.delete()
        return Response({"status": "success", "data": "Wish list has been deleted"})

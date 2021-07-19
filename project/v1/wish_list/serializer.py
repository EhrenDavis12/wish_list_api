from django.db import models
from rest_framework import serializers
from project.models import WishList


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ["id", "name", "created", "last_updated"]
        read_only_fields = ["id", "name", "created", "last_updated"]


class WishListWriteSerializer(serializers.ModelSerializer):
    # name = models.CharField(max_length=256, blank=False)

    class Meta:
        model = WishList
        fields = ["id", "name"]
        read_only_fields = ["id", "created", "last_updated"]

from rest_framework import serializers
from project.models import WishList


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ["id", "name", "public_note", "private_note", "created", "last_updated"]
        read_only_fields = ["id", "created", "last_updated"]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(WishListSerializer, self).create(validated_data)

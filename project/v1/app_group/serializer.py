from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from project.models import AppGroup, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ["user", "nick_name", "is_admin"]


class AppGroupSerializer(serializers.ModelSerializer):
    users = GroupMemberSerializer(source='groupmember_set', many=True, read_only=False, default=None, allow_null=True)

    class Meta:
        model = AppGroup
        fields = ["id", "name", "description", "is_active", "created", "last_updated", "users"]
        read_only_fields = ["id", "created", "last_updated"]
        extra_kwargs = {'users': {'required': False}}

    def create(self, validated_data):
        validated_data.pop('groupmember_set', None)  # only creator can be assigned for now
        app_group = super(AppGroupSerializer, self).create(validated_data)
        GroupMember.objects.create(
            user=self.context['request'].user,
            app_group=app_group,
            is_admin=True
        )
        return app_group

    def _validate_update(self, instance, validated_data):
        user_id = self.context['request'].user.id
        user = instance.groupmember_set.filter(user=user_id, is_admin=True)
        if user.count() < 1:
            # raise ValidationError(_('User is not admin'), code='Unauthorized')
            raise ValidationError('User can not make changes to this group', code='Unauthorized')

    def update(self, instance, validated_data):
        self._validate_update(instance, validated_data)
        users = validated_data.pop('groupmember_set', None)
        instance = super(AppGroupSerializer, self).update(instance, validated_data)
        keep_groups_ids = []
        if users:
            user_ids = [x["user"].id for x in users]
            if self.context['request'].user.id not in user_ids:
                users.append({"user": self.context['request'].user.id})

            for data in users:
                user = data.pop('user', None)
                group_member, created = GroupMember.objects.update_or_create(
                    user=user,
                    app_group=instance,
                    defaults=data
                )
                keep_groups_ids.append(group_member.id)

            instance.groupmember_set.exclude(id__in=keep_groups_ids).delete()
        return instance

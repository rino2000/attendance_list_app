from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "is_team_leader", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)

        if not user.is_team_leader:
            content_type = ContentType.objects.get(
                app_label__iexact="users", model__iexact="CustomUser"
            )
            permission_to_remove = Permission.objects.get(
                codename="can_create_team",
                content_type=content_type,
            )
            user.user_permissions.remove(permission_to_remove)

        user.set_password(password)
        user.save()
        return user

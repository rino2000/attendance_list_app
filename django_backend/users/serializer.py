from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import CustomUser


class CustomUserLoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username, password = data.get("username"), data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "is_team_leader", "password")
        extra_kwargs = {"password": {"write_only": True}}

    # def create(self, validated_data: dict):
    #     password = validated_data.pop("password")
    #     user = CustomUser.objects.create(**validated_data)

    #     if not user.is_team_leader:
    #         content_type = ContentType.objects.get(
    #             app_label__iexact="users", model__iexact="CustomUser"
    #         )
    #         permission_to_remove = Permission.objects.get(
    #             codename="can_create_team",
    #             content_type=content_type,
    #         )
    #         user.user_permissions.remove(permission_to_remove)

    #     user.set_password(password)
    #     user.save()
    #     return user

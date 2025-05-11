from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "is_team_leader",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "is_team_leader", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_team_leader=validated_data["is_team_leader"],
        )

        # if not user.is_team_leader:
        #     content_type = ContentType.objects.get(
        #         app_label__iexact="users", model__iexact="CustomUser"
        #     )
        #     permission_to_remove = Permission.objects.get(
        #         codename="can_create_team",
        #         content_type=content_type,
        #     )
        #     user.user_permissions.remove(permission_to_remove)

        user.set_password(validated_data["password"])
        user.save()
        return user

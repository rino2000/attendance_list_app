from rest_framework.generics import CreateAPIView

from .models import CustomUser
from .serializer import CustomUserSerializer


class CreateUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        # is_team_leader = self.request.POST["is_team_leader"]

        # if is_team_leader:
        #     content_type = ContentType.objects.get_for_model(CustomUser)
        #     permission = Permission.objects.get(
        #         codename="can_create_team",
        #         content_type=content_type,
        #     )
        #     request

        return self.create(request, *args, **kwargs)

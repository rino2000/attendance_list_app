from rest_framework.generics import CreateAPIView

from .models import CustomUser
from .serializer import CustomUserSerializer


class CreateUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

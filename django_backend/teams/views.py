from rest_framework import generics
from rest_framework.response import Response
from .models import Team
from .serializer import TeamSerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly


class IsTeamLeader(BasePermission):
    def has_permission(self, request, view) -> bool:
        print(request.user)
        print(request.user.is_team_leader)
        return True if request.user.has_perm("users.can_create_team") else False


class CreateTeamView(generics.CreateAPIView):
    model = Team.objects.all()
    serializer_class = TeamSerializer
    # permission_classes = [IsTeamLeader, IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        if request.context["team"] is None:
            return Response({"error": "team field is not set"})
        print(request)
        return super().post(request, *args, **kwargs)

from rest_framework import generics
from .models import Team
from .serializer import TeamSerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly


class IsTeamLeader(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.has_perm("users.can_create_team") else False


class CreateTeamView(generics.CreateAPIView):
    model = Team.object.all()
    serializer_class = TeamSerializer
    permission_classes = [IsTeamLeader, IsAuthenticatedOrReadOnly]

from django.db import models
from users.models import CustomUser


class Team(models.Model):
    team = models.SmallIntegerField(blank=False, null=False, unique=True)
    team_leader = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ManyToManyField(CustomUser, related_name="employees")

    def __str__(self) -> str:
        return f"Team({self.team} team_leader: {self.team_leader} empyloyees: {self.employee})"

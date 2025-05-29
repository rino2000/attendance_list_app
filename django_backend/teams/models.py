from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError


class Team(models.Model):
    team = models.SmallIntegerField(blank=False, null=False, unique=True)
    team_leader = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    employee = models.ManyToManyField(CustomUser, related_name="employees")

    def __str__(self) -> str:
        return f"Team({self.team} team_leader: {self.team_leader} empyloyees: {self.employee.all()})"

    def save(self, *args, **kwargs):
        if not bool(self.team_leader.is_team_leader):
            raise ValidationError("User must be a team leader")
        super().save(*args, **kwargs)

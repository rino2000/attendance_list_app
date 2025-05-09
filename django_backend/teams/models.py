from django.db import models
from users.models import CustomUser


class Team(models.Model):
    team = models.SmallIntegerField(blank=False, null=False, unique=True)
    team_leader = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employees = models.ManyToManyField(
        CustomUser, related_name="%(app_label)s_%(class)s_related"
    )

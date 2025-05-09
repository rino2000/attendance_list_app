from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, max_length=50, null=False, blank=False)
    password = models.CharField(max_length=80, null=False, blank=False)
    is_team_leader = models.BooleanField(null=False, blank=False, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self) -> str:
        return f"CustomUser(email: {self.email} team: {self.team} is team leader: {self.is_team_leader})"

    @property
    def is_team_lead(self) -> bool:
        return self.is_team_leader

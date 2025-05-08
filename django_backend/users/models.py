from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    roles = (("teamleader", "TeamLeader"), ("employee", "Employee"))
    user_role = models.CharField(
        choices=roles, default="employee", null=False, blank=False
    )
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, max_length=50, null=False, blank=False)
    password = models.CharField(max_length=80, null=False, blank=False)
    team = models.PositiveSmallIntegerField(null=False, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self) -> str:
        return f"User({self.email} {self.team})"

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
        return f"CustomUser(id: {self.pk} email: {self.email} is team leader: {self.is_team_leader})"

    @property
    def is_team_lead(self) -> bool:
        return self.is_team_leader


class Attendance(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        choices=[("present", "Present"), ("absent", "Absent")], default="present"
    )
    reason = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"Attendance(CustomUser id: {self.employee.pk} date: {self.date} reason: {self.reason})"

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EmailValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    username == email
    """

    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    is_team_leader = models.BooleanField(null=False, blank=False)
    username = models.EmailField(
        unique=True, blank=False, null=False, validators=[EmailValidator()]
    )

    REQUIRED_FIELDS = ["password"]

    class Meta:
        permissions = (("can_create_team", "Can create Team (only Team leaders)"),)

    def __str__(self) -> str:
        return f"CustomUser(id: {self.pk} email: {self.username} is team leader: {self.is_team_leader})"

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

        content_type = ContentType.objects.get(
            app_label__iexact="users", model__iexact="CustomUser"
        )
        can_create_team_permission = Permission.objects.get(
            codename="can_create_team",
            content_type=content_type,
        )

        # if field [is_team_leader] is False than remove permission [can_create_team]
        if not bool(self.is_team_leader):
            self.user_permissions.remove(can_create_team_permission)
        else:
            self.user_permissions.add(can_create_team_permission)


class Attendance(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        choices=[("present", "Present"), ("absent", "Absent")], default="present"
    )
    reason = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"Attendance(CustomUser id: {self.employee.pk} date: {self.date} reason: {self.reason})"

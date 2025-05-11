from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Attendance, CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        team_leader = CustomUser(
            first_name="test1",
            last_name="test1",
            username="test1@test.com",
            is_team_leader=True,
        )
        team_leader.set_password("test")
        team_leader.save()

        employee = CustomUser(
            first_name="test2",
            last_name="test2",
            username="test2@test.com",
            is_team_leader=False,
        )
        employee.set_password("test")
        employee.save()

    def test_password_hashed(self):
        teamleader = CustomUser.objects.get(username="test1@test.com")
        employee = CustomUser.objects.get(username="test2@test.com")

        self.assertNotEqual(teamleader.password, "test")
        self.assertNotEqual(employee.password, "test")

        self.assertTrue(teamleader.password.startswith("pbkdf2_sha256$"))
        self.assertTrue(employee.password.startswith("pbkdf2_sha256$"))

    def test_create_team_leader(self):
        teamleader = CustomUser.objects.get(username="test1@test.com")
        employee = CustomUser.objects.get(username="test2@test.com")

        self.assertEqual(teamleader.username, "test1@test.com")
        self.assertEqual(teamleader.is_team_leader, True)

        self.assertEqual(employee.username, "test2@test.com")
        self.assertEqual(employee.is_team_leader, False)

    def test_add_user_to_attendance(self):
        employee = CustomUser.objects.get(username="test2@test.com")

        attendance = Attendance.objects.create(
            employee_id=employee.pk, reason="test reason"
        )

        import datetime

        self.assertEqual(attendance.date, datetime.date.today())
        self.assertEqual(attendance.reason, "test reason")
        self.assertEqual(attendance.employee.pk, employee.pk)

    def test_permission_if_custom_user_is_team_leader(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(CustomUser)
        permission = Permission.objects.get(
            content_type=content_type, codename="can_create_team"
        )

        emp = CustomUser.objects.get(username="test1@test.com")
        emp.save()
        emp.user_permissions.add(permission)


class TestApi(APITestCase):

    def test_create_custom_user(self):
        data = {
            "username": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": True,
        }

        response = self.client.post("/api/user/create", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(
            CustomUser.objects.get(username="test@test.com").username, "test@test.com"
        )

        response = self.client.post(path="/api/user/create", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(CustomUser.objects.filter(username="test@test.com").exists())

        employee = {
            "first_name": "test",
            "last_name": "test",
            "username": "test111@test.com",
            "password": "test",
            "is_team_leader": False,
        }

        response = self.client.post(
            path="/api/user/create", data=employee, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="test111@test.com").exists())
        self.assertEqual(CustomUser.objects.all().count(), 2)

    def test_if_password_is_hashed(self):
        data = {
            "username": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": True,
        }

        response = self.client.post("/api/user/create", data, format="json")

        team_leader = CustomUser.objects.get(username="test@test.com")
        print(team_leader.password)
        self.assertTrue(team_leader.password.startswith("pbkdf2_sha256$"))

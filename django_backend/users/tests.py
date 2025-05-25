from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Attendance, CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.team_leader = CustomUser(
            first_name="test1",
            last_name="test1",
            username="test1@test.com",
            is_team_leader=True,
        )
        self.team_leader.set_password("test")
        self.team_leader.save()

        self.employee = CustomUser(
            first_name="test2",
            last_name="test2",
            username="test2@test.com",
            is_team_leader=False,
        )
        self.employee.set_password("test")
        self.employee.save()

    def test_password_hashed(self):
        self.assertNotEqual(self.team_leader.password, "test")
        self.assertNotEqual(self.employee.password, "test")

        self.assertTrue(self.team_leader.password.startswith("pbkdf2_sha256$"))
        self.assertTrue(self.employee.password.startswith("pbkdf2_sha256$"))

    def test_create_team_leader(self):
        self.assertEqual(self.team_leader.username, "test1@test.com")
        self.assertEqual(self.team_leader.is_team_leader, True)

        self.assertEqual(self.employee.username, "test2@test.com")
        self.assertEqual(self.employee.is_team_leader, False)

    def test_add_user_to_attendance(self):
        attendance = Attendance.objects.create(
            employee_id=self.employee.pk, reason="test reason"
        )

        import datetime

        self.assertEqual(attendance.date, datetime.date.today())
        self.assertEqual(attendance.reason, "test reason")
        self.assertEqual(attendance.employee.pk, self.employee.pk)


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

    def test_password_hash_over_api(self):
        data = {
            "username": "test2222@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": True,
        }

        response = self.client.post("/api/user/create", data, format="json")

        print(response.json())

        team_leader = CustomUser.objects.get(username="test2222@test.com")
        print(f"team_leader hashed password over api == {team_leader.password}")

        self.assertTrue(team_leader.password.startswith("pbkdf2_sha256$"))

    def test_user_can_not_create_team_permission(self):
        data = {
            "username": "test123@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": False,
        }

        self.client.post("/api/user/create", data, format="json")

        customUser = CustomUser.objects.get(username="test123@test.com")

        self.assertFalse(customUser.has_perm("users.can_create_team"))

    def test_team_leader_has_permission_to_create_team(self):
        data = {
            "username": "test123456@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": True,
        }

        self.client.post("/api/user/create", data, format="json")

        team_leader = CustomUser.objects.get(username="test123456@test.com")
        print(team_leader.has_perm("users.can_create_team"))

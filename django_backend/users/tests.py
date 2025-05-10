from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Attendance, CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        team_leader = CustomUser(
            first_name="test1",
            last_name="test1",
            email="test1@test.com",
            username="test1",
            is_team_leader=True,
        )
        team_leader.set_password("test")
        team_leader.save()

        employee = CustomUser(
            first_name="test2",
            last_name="test2",
            email="test2@test.com",
            username="test2",
            is_team_leader=False,
        )
        employee.set_password("test")
        employee.save()

    def test_password_hashed(self):
        teamleader = CustomUser.objects.get(email="test1@test.com")
        employee = CustomUser.objects.get(email="test2@test.com")

        self.assertNotEqual(teamleader.password, "test")
        self.assertNotEqual(employee.password, "test")

        self.assertTrue(teamleader.password.startswith("pbkdf2_sha256$"))
        self.assertTrue(employee.password.startswith("pbkdf2_sha256$"))

    def test_create_team_leader(self):
        teamleader = CustomUser.objects.get(email="test1@test.com")
        employee = CustomUser.objects.get(email="test2@test.com")

        self.assertEqual(teamleader.email, "test1@test.com")
        self.assertEqual(teamleader.is_team_leader, True)

        self.assertEqual(employee.email, "test2@test.com")
        self.assertEqual(employee.is_team_leader, False)

    def test_add_user_to_attendance(self):
        employee = CustomUser.objects.get(email="test2@test.com")

        attendance = Attendance.objects.create(
            employee_id=employee.pk, reason="test reason"
        )

        import datetime

        self.assertEqual(attendance.date, datetime.date.today())
        self.assertEqual(attendance.reason, "test reason")
        self.assertEqual(attendance.employee.pk, employee.pk)


class TestApi(APITestCase):

    def test_create_custom_user(self):
        data = {
            "username": "test123",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "password": "test",
            "is_team_leader": True,
        }

        response = self.client.post("/api/user/create", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(
            CustomUser.objects.get(email="test@test.com").email, "test@test.com"
        )

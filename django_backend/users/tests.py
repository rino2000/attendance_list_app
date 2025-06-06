from django.test import TestCase
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.test import AsyncClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from teams.models import Team

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

        return super().setUp()

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

    def setUp(self):
        self.team_leader = {
            "username": "test123@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": True,
        }

        self.user = {
            "username": "test111@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "is_team_leader": False,
        }

        self.async_client = AsyncClient()

    async def test_create_user(self):
        response: HttpResponse = await self.async_client.post(
            path="/api/user/create", data=self.user, format="json"
        )

        user = await CustomUser.objects.aget(username=self.user.get("username"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(await CustomUser.objects.acount(), 1)

        self.assertTrue(not user.is_team_leader)
        self.assertTrue(user.password.startswith("pbkdf2_sha256$"))

    async def test_create_team_leader(self):
        response: HttpResponse = await self.async_client.post(
            path="/api/user/create", data=self.team_leader, format="json"
        )

        team_leader = await CustomUser.objects.aget(
            username=self.team_leader.get("username")
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(team_leader.password.startswith("pbkdf2_sha256$"))

        self.assertTrue(team_leader.is_team_leader)
        self.assertTrue(await team_leader.ahas_perm("users.can_create_team"))

    async def test_user_has_not_create_team_permission(self):
        await self.async_client.post("/api/user/create", data=self.user, format="json")

        customUser = await CustomUser.objects.aget(username=self.user.get("username"))

        self.assertFalse(await customUser.ahas_perm("users.can_create_team"))

    async def test_user_create_team_exception(self):
        await self.async_client.post("/api/user/create", data=self.user, format="json")

        user = await CustomUser.objects.aget(username=self.user.get("username"))
        team = Team(team=1234, team_leader=user)

        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError) as error:
            team.save()

        self.assertEqual(error.exception.message, "User must be a team leader")
        self.assertFalse(user.is_team_leader)
        self.assertFalse(await user.ahas_perm("users.can_create_team_leader"))

    async def test_user_get_token(self):
        response: HttpResponse = await self.async_client.post(
            "/api/user/create", data=self.user, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response: HttpResponse = await self.async_client.post(
            path=reverse("api_token_auth"),
            data={
                "username": self.user.get("username"),
                "password": self.user.get("password"),
            },
            format="json",
        )

        user = await CustomUser.objects.aget(username=self.user.get("username"))
        token = await sync_to_async(Token.objects.get)(user=user)

        self.assertEqual(response.data["token"], token.key)
        self.assertIn("token", response.data)

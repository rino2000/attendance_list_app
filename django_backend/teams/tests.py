from django.test import TestCase
from django.http import HttpResponse
from django.test import AsyncClient
from rest_framework.test import APITestCase
from users.models import CustomUser

from .models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        self.team_leader = CustomUser.objects.create(
            first_name="test1",
            last_name="test1",
            username="test1@test.com",
            password="test",
            is_team_leader=True,
        )

        self.user_1 = CustomUser.objects.create(
            first_name="test2",
            last_name="test2",
            username="test2@test.com",
            password="test",
            is_team_leader=False,
        )

        self.user_2 = CustomUser.objects.create(
            first_name="test3",
            last_name="test3",
            password="test",
            username="test3@test.com",
            is_team_leader=False,
        )

        self.team = Team.objects.create(team=1111, team_leader=self.team_leader)

    def test_team_employees_empty(self):
        self.assertTrue(self.team.employee.count() == 0)

    def test_create_team(self):
        self.assertEqual(self.team.team, 1111)
        self.assertEqual(self.team_leader.username, self.team_leader.username)
        self.assertEqual(self.team.employee.count(), 0)

    def test_add_employees_in_team(self):
        self.team.employee.add(self.user_1.pk)
        self.team.employee.add(self.user_2.pk)

        self.assertIn(self.user_1, self.team.employee.all())
        self.assertIn(self.user_2, self.team.employee.all())
        self.assertEqual(2, self.team.employee.count())


# class CreateTeamTest(APITestCase):
#     def setUp(self):
#         self.team_leader_data = {
#             "username": "test@test.com",
#             "first_name": "test",
#             "last_name": "test",
#             "password": "test",
#             "is_team_leader": True,
#         }

#         self.user_data = {
#             "username": "test1@test.com",
#             "first_name": "test",
#             "last_name": "test",
#             "password": "test",
#             "is_team_leader": False,
#         }

#         self.async_client = AsyncClient()

#     async def test_create_team(self):
#         response: HttpResponse = await self.async_client.post(
#             path="/api/user/create", data=self.user_data, format="json"
#         )
#         self.assertEqual(response.status_code, 201)

#         response: HttpResponse = await self.async_client.post(
#             path="/api/user/create", data=self.team_leader_data, format="json"
#         )
#         self.assertEqual(response.status_code, 201)

#         team_leader = await CustomUser.objects.aget(username="test@test.com")

#         response: HttpResponse = await self.async_client.post(
#             path="api/team/create",
#             data={"team": 123, "team_leader": team_leader},
#             format="json",
#         )

#         print(response.context)
#         print(response)

# response: HttpResponse = await self.async_client.post(
#     path="/api/token",
#     data={
#         "username": team_leader.username,
#         "password": self.team_leader_data["password"],
#     },
#     format="json",
# )

# response: HttpResponse = await self.async_client.post(
#     path="/api/token",
#     data={
#         "username": team_leader.username,
#         "password": self.team_leader_data["password"],
#     },
#     format="json",
# )

# print(response.content)

# self.team_data = {"team": 123, "team_leader": team_leader.pk}

# response = await self.async_client.post(
#     path="/api/team/create", data=self.team_data, format="json"
# )

# print(response)
# print(response.content)
# self.assertEqual(response.status_code, 201)

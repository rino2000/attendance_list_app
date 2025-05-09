from django.test import TestCase
from users.models import CustomUser

from .models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            first_name="test1",
            last_name="test1",
            email="test1@test.com",
            password="test",
            username="test1",
            is_team_leader=True,
        )

        CustomUser.objects.create(
            first_name="test2",
            last_name="test2",
            email="test2@test.com",
            password="test",
            username="test2",
            is_team_leader=False,
        )

        CustomUser.objects.create(
            first_name="test3",
            last_name="test3",
            email="test3@test.com",
            password="test",
            username="test3",
            is_team_leader=False,
        )

    def test_create_team(self):
        teamleader = CustomUser.objects.get(email="test1@test.com")
        employee = CustomUser.objects.get(email="test2@test.com")
        employee2 = CustomUser.objects.get(email="test2@test.com")

        t = Team.objects.create(team=1111, team_leader=teamleader)
        t.employees.add(employee2)

        self.assertEqual(t.team_leader, teamleader)

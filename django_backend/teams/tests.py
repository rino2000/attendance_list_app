from django.test import TestCase
from users.models import CustomUser

from .models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            first_name="test1",
            last_name="test1",
            username="test1@test.com",
            password="test",
            is_team_leader=True,
        )

        CustomUser.objects.create(
            first_name="test2",
            last_name="test2",
            username="test2@test.com",
            password="test",
            is_team_leader=False,
        )

        CustomUser.objects.create(
            first_name="test3",
            last_name="test3",
            password="test",
            username="test3@test.com",
            is_team_leader=False,
        )

        Team.objects.create(
            team=1111, team_leader=CustomUser.objects.get(username="test1@test.com")
        )

    def test_team_employees_empty(self):
        t = Team.objects.first()
        self.assertTrue(t.employee.count() == 0)

    def test_create_team(self):
        t = Team.objects.first()
        self.assertEqual(t.team, 1111)
        self.assertEqual(
            t.team_leader, CustomUser.objects.get(username="test1@test.com")
        )
        self.assertEqual(t.employee.count(), 0)

    def test_add_employees_in_team(self):
        employee2 = CustomUser.objects.get(username="test2@test.com")
        employee3 = CustomUser.objects.get(username="test3@test.com")
        t = Team.objects.first()

        t.employee.add(employee2.pk)
        t.employee.add(employee3.pk)

        self.assertIn(employee2, t.employee.all())
        self.assertIn(employee3, t.employee.all())
        self.assertEqual(2, t.employee.count())

from django.test import TestCase

from .models import CustomUser


class CustomUserTestCase(TestCase):
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

    def test_create_team_leader(self):
        teamleader = CustomUser.objects.get(email="test1@test.com")
        employee = CustomUser.objects.get(email="test2@test.com")

        self.assertEqual(teamleader.email, "test1@test.com")
        self.assertEqual(teamleader.is_team_leader, True)

        self.assertEqual(employee.email, "test2@test.com")
        self.assertEqual(employee.is_team_leader, False)

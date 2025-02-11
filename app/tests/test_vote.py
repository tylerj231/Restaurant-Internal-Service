from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from app.models import Vote, DailyMenu, Restaurant
from app.serializers import VoteSerializer


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test123",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_votes(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        Vote.objects.create(employee=self.user, voted_at=timezone.now(), menu=menu)
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        url = reverse("app:vote-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_vote_allowed_for_employee(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        payload = {
            "employee": self.user,
            "voted_at": timezone.now(),
            "menu": menu.id,
        }
        url = reverse("app:vote-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_vote_allowed_for_employee(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        vote = Vote.objects.create(
            employee=self.user,
            voted_at=timezone.now(),
            menu=menu,
        )
        url = reverse("app:vote-detail", args=[vote.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

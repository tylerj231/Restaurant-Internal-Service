from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


BASE_URL =  reverse("app:restaurant-list")
DETAIL_URL = reverse("app:restaurant-detail", args=[1,])

class UnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        response = self.client.get(BASE_URL)
        response_detail = self.client.get(DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_detail.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.models import Restaurant
from app.serializers import RestaurantSerializer


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test123",

        )
        self.client.force_authenticate(user=self.user)

    def test_get_restaurant(self):
        Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        url = reverse('app:restaurant-list')
        response = self.client.get(url)
        restautrants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restautrants, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_restaurant_forbidden_for_employee(self):
        url = reverse('app:restaurant-list')
        payload = {
            "name": "Macdonald",
            "address": "123 Main St.",
            "contact_information": "123-444-55",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_restaurant_forbidden_for_employee(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        url = reverse('app:restaurant-detail', args=[restaurant.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_restaurant_allow(self):
        self.user.is_staff = True
        self.user.save()
        payload = {
            "name": "Macdonald",
            "address": "123 Main St.",
            "contact_information": "123-444-55",
        }

        url = reverse("app:restaurant-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_restaurant_allow(self):
        self.user.is_staff = True
        self.user.save()
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )

        url = reverse("app:restaurant-detail", args=[restaurant.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

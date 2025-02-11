from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.models import MenuItem, DailyMenu, Restaurant
from app.serializers import (
    MenuItemSerializer,
    DailyMenuSerializer,
    RestaurantSerializer,
)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test123",
        )
        self.client.force_authenticate(user=self.user)

    def test_menu_item_list(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        daily_menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        menu_item = MenuItem.objects.create(
            name="Burger",
            price=10,
            category="Burgers",
            dietary_information="non-vegan",
            daily_menu=daily_menu,
        )
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)

        url = reverse("app:menuitem-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_menu_create_forbidden_for_employee(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        daily_menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )

        payload = {
            "name": "Burger",
            "price": 10,
            "category": "Burgers",
            "dietary_information": "non-vegan",
            "daily_menu": daily_menu,
        }
        url = reverse("app:menuitem-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_menu_delete_forbidden_for_employee(self):
        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        daily_menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        menu_item = MenuItem.objects.create(
            name="Burger",
            price=10,
            category="Burgers",
            dietary_information="non-vegan",
            daily_menu=daily_menu,
        )
        url = reverse("app:menuitem-list")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_menu_item_allow(self):
        self.user.is_staff = True
        self.user.save()

        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )

        daily_menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )

        payload = {
            "name": "Burger",
            "price": 10,
            "category": "Burgers",
            "dietary_information": "non-vegan",
            "daily_menu": daily_menu.id,
        }

        url = reverse("app:menuitem-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_menu_item_allow(self):
        self.user.is_staff = True
        self.user.save()

        restaurant = Restaurant.objects.create(
            name="Macdonald",
            address="123 Main St.",
            contact_information="123-444-55",
        )
        daily_menu = DailyMenu.objects.create(
            date=timezone.now().date(),
            is_active=True,
            restaurant=restaurant,
        )
        menu_item = MenuItem.objects.create(
            name="Burger",
            price=10,
            dietary_information="non-vegan",
            category="Burgers",
            daily_menu=daily_menu,
        )

        url = reverse("app:menuitem-detail", args=[menu_item.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Restaurant, DailyMenu, MenuItem, Vote

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id", "name", "price", "category", "dietary_information", "daily_menu")

class MenuItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("name",)

class DailyMenuSerializer(serializers.ModelSerializer):
    menu_item = MenuItemListSerializer(many=True, read_only=True)
    restaurant = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Restaurant.objects.all()
    )

    class Meta:
        model = DailyMenu
        fields = ("id", "date", "is_active", "restaurant", "menu_item")

class DailyMenuListSerializer(serializers.ModelSerializer):
    menu_item = MenuItemListSerializer(many=True, read_only=True)

    class Meta:
        model = DailyMenu
        fields = ("is_active", "menu_item",)

class RestaurantSerializer(serializers.ModelSerializer):
    daily_menu = DailyMenuListSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ("id", "name", "contact_information", "address", "daily_menu")
        read_only_fields = ("id",)

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("menu", "voted_at")
        read_only_fields = ("voted_at",)

    def validate(self, data):
        menu = data["menu"]
        employee = self.context["request"].user

        if Vote.objects.filter(menu=menu, employee=employee).exists():
            raise ValidationError("You already voted for this menu")

        if timezone.now().hour >= 13:
            raise ValidationError("Voting is possible until lunch time (1 PM) ")

        return data

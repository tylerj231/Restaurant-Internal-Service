from rest_framework import serializers

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
    menu = DailyMenuListSerializer(many=False, read_only=True)
    class Meta:
        model = Vote
        fields = ("menu", "voted_at")

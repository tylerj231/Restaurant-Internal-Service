from django.utils import timezone

from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import Employee


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="daily_menu"
    )

    date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("restaurant", "date")

    def __str__(self):
        return f"{self.restaurant.name} menu"


class MenuItem(models.Model):
    daily_menu = models.ForeignKey(
        DailyMenu, on_delete=models.CASCADE, related_name="menu_item"
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=100)
    dietary_information = models.CharField(max_length=100)


class Vote(models.Model):
    TIME_NOW = timezone.now().hour
    menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE, related_name="votes")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes"
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("menu", "employee")

    def clean(self):
        if not self.menu.is_active:
            raise ValidationError("Menu is not active")
        if self.menu.date != timezone.now().date():
            raise ValidationError("Can only vote for today's menu")

        if self.TIME_NOW >= 13:
            raise ValidationError("Voting is possible until lunch time")

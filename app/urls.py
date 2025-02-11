from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views

app_name = "app"
router = DefaultRouter()
router.register("restaurants", views.RestaurantViewSet, basename="restaurant")
router.register("menus", views.DailyMenuViewSet, basename="menus")
router.register("menu-items", views.MenuItemViewSet, basename="menu-items")

router.register("votes", views.VoteViewSet, basename="vote")
router.register("most-voted", views.MostVotedMenuViewSet, basename="most-voted")
urlpatterns = [
    path("", include(router.urls)),
]

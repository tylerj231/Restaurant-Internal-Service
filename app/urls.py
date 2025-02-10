from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views

app_name = 'app'
router = DefaultRouter()
router.register("restaurants", views.RestaurantViewSet)
router.register("menus", views.DailyMenuViewSet)
router.register("menu-items", views.MenuItemViewSet)

router.register("votes", views.VoteViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

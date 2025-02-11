from django.db.models import Count
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Restaurant, DailyMenu, MenuItem, Vote
from app.permissions import IsAdminOrIfAuthenticatedReadOnly

from app.serializers import (
    RestaurantSerializer,
    DailyMenuSerializer,
    MenuItemSerializer,
    VoteSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class DailyMenuViewSet(viewsets.ModelViewSet):
    queryset = DailyMenu.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    serializer_class = DailyMenuSerializer

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get("date", None)

        if date:
            queryset = queryset.filter(date=date)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date",
                type=str,
                description="Filter daily menu by date: Ex. ?date=2025-02-10",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def get_queryset(self):
        queryset = Vote.objects.filter(employee=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class MostVotedMenuViewSet(viewsets.ModelViewSet):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer

    @action(detail=False, methods=["get"])
    def most_voted(self, request):
        today = timezone.now().date()

        most_voted_menu = (
            DailyMenu.objects.filter(date=today, is_active=True)
            .annotate(vote_count=Count("votes"))
            .order_by("-vote_count")
            .first()
        )

        if not most_voted_menu:
            return Response(
                {"message": "No votes for today"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(most_voted_menu)
        return Response(
            {
                "restaurant": most_voted_menu.restaurant.name,
                "vote_count": most_voted_menu.vote_count,
                "menu": serializer.data,
            }
        )

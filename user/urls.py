from django.urls import path

from user.views import CreateEmployeeView, ManageEmployeeView

app_name = "user"
urlpatterns = [
    path("register/", CreateEmployeeView.as_view(), name="create"),
    path("me/", ManageEmployeeView.as_view(), name="manage"),
]

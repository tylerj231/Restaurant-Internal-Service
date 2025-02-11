from rest_framework import generics

from user.serializers import EmployeeSerializer


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer


class ManageEmployeeView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployeeSerializer

    def get_object(self):
        return self.request.user

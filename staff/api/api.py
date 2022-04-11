from staff.models import Employee
from rest_framework.generics import ListAPIView
from staff.api.serializers import EmployeeSerializer
from .permissions import IsTopManegment
from rest_framework.permissions import IsAdminUser


class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser | IsTopManegment]

    @classmethod
    def get_extra_actions(cls):
        return []


class EmployeeOneLevelListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser | IsTopManegment]

    def get_queryset(self):
        level = self.kwargs['level']
        return Employee.objects.filter(level=level)

    @classmethod
    def get_extra_actions(cls):
        return []

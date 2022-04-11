from staff.models import Employee
from rest_framework.generics import ListAPIView
from staff.api.serializers import EmployeeSerializer
from .permissions import IsTopManagement
from rest_framework.permissions import IsAdminUser


class EmployeeListView(ListAPIView):
    """
    API-представление, доступное только для администраторов (is_stuff) и группы permissions Top Management
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser | IsTopManagement]

    @classmethod
    def get_extra_actions(cls):
        return []


class EmployeeOneLevelListView(ListAPIView):
    """
    API-представление, доступное только для администраторов (is_stuff) и группы permissions Top Management
    Отображает только сотрудников одного уровня (level), указанного в запросе 0 - 4
    Если указано > 4, то возвращается []
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser | IsTopManagement]

    def get_queryset(self):
        level = self.kwargs['level']
        return Employee.objects.filter(level=level)

    @classmethod
    def get_extra_actions(cls):
        return []

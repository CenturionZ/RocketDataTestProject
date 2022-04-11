from rest_framework import serializers
from staff.models import Employee, Position

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
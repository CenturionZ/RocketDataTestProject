from django.urls import path, include
from staff.api.api import *

urlpatterns = [
    path('', EmployeeListView.as_view()),
    path('level/<int:level>', EmployeeOneLevelListView.as_view()),
    path('', include('rest_framework.urls')),
]
from django.shortcuts import render
from .models import Employee


def index(request):
    return render(request, "test_template.html",
                  {'nodes': Employee.objects.all()})

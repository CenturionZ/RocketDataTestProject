from django import forms
from .models import Employee, Payment


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'parent', 'position']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['employee', 'payment', 'payment_date']

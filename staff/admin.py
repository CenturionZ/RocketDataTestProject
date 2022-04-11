from django.contrib import admin
from django.contrib.auth.models import User

from .models import Employee, Payment, Position
from mptt.admin import DraggableMPTTAdmin
from django import forms

from .tasks import delete_employee_payments_history


class PaymentsManager(admin.TabularInline):
    model = Payment
    extra = 0


class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['user'].help_text = 'test'

    class Meta:
        model = Employee
        exclude = ('',)


class StaffAdmin(DraggableMPTTAdmin):
    form = StaffForm
    # fields = ('name', 'salary')
    list_display = ('tree_actions', 'indented_title', 'name', 'position', 'parent', 'salary', 'sum_payments')
    list_display_links = ('indented_title', 'parent')
    list_filter = ('level', 'position')
    readonly_fields = ('start_date', )
    inlines = (PaymentsManager, )
    actions = ('delete_payments_history',)

    @admin.action(description='Удалить историю выплат выбранных сотрудников')
    def delete_payments_history(sefl, request, queryset):
        if len(queryset) <= 20:
            for obj in queryset:
                Payment.objects.filter(employee_id=obj.id).delete()
        else:
            for employee in queryset:
                delete_employee_payments_history.delay(employee.id)

    def sum_payments(self, obj):
        return obj.get_payments()


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payment', 'payment_date')
    readonly_fields = ('payment_date',)


admin.site.register(Employee, StaffAdmin)
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(Position)

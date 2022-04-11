from __future__ import absolute_import, unicode_literals

from celery import current_app
from celery import shared_task
from celery.schedules import crontab
from django.utils import timezone

from .forms import PaymentForm
from .models import Employee, Payment


# @current_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(crontab(minute=0, hour='*/2'),
#                              pay_employers_task.s(),
#                              name='Pay employers')


@shared_task
def pay_employers_task():
    """
    Выплата сотрудникам (Employee) соразмерная их зарплатам (salary).
    Таск устанавливается в админ-панели celery-beat-schedule.
    """
    staff = Employee.objects.all()

    for employee in staff:
        form = PaymentForm(data={
            'employee': employee.id,
            'payment': employee.salary,
            'payment_date': timezone.now(),
        })
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        else:
            print('Data in not valid')


@shared_task
def delete_employee_payments_history(id: int):
    """
    Делает выборку платежей (Payment) одного сотрудника (employee.id) и удаляет эти записи.
    :param id: идентификатор пользователя
    """
    Payment.objects.filter(employee_id=id).delete()

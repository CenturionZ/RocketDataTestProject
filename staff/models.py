from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import PermissionsMixin

from mptt.models import MPTTModel, TreeForeignKey


class Position(models.Model):
    position_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.position_name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Employee(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250, unique=False, verbose_name='ФИО')
    salary = models.FloatField(default=0.0, verbose_name='Размер заработной платы')
    start_date = models.DateField(auto_now_add=False,
                                  default=timezone.now,
                                  verbose_name='Дата приёма на работу')
    date_added = models.DateTimeField(auto_now_add=True)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 related_name='position',
                                 verbose_name='Должность', blank=False, null=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            verbose_name='Начальник')

    # def get_full_name(self):
    #     '''
    #     Returns the first_name plus the last_name, with a space in between.
    #     '''
    #     return f'{self.user.first_name} {self.user.last_name} {self.third_name}'
    #
    # def get_short_name(self):
    #     '''
    #     Returns the short name for the user.
    #     '''
    #     return self.first_name

    def __str__(self):
        return f'Level {self.get_level()}'

    def get_payments(self):
        return sum([item.payment for item in self.payee.get_queryset()])

    def save(self, *args, **kwargs):
        if self.parent == None:
            super(Employee, self).save(*args, **kwargs)
            return
        elif self.parent.level == 4:
            raise ValueError(u'Достигнута максимальная вложенность!')
        super(Employee, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'


class Payment(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 related_name='payee',
                                 verbose_name='Получатель')
    payment = models.FloatField(default=0.0, verbose_name='Размер выплаты')
    payment_date = models.DateField(auto_now_add=False,
                                    default=timezone.now,
                                    verbose_name='Дата выплаты')

    def __str__(self):
        return f'{self.employee.name} получил {self.payment}'

    class Meta:
        verbose_name = 'Выплаты'
        verbose_name_plural = 'Выплаты'

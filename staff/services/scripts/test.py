from staff.forms import EmployeeForm
from staff.models import Payment, Position, Employee

# somtething = Position.objects.all()
#
# for item in somtething:
#     print(item.id)
#
# print(somtething)
#
# test = {'a': 1, 'b': 2}
# print(len(test))
# print(test.items())

for i in range(2):
    form = EmployeeForm(data={
            'name': 'AAA',
            'parent': Employee.objects.last().id,
        })
    form.save()
    print(Employee.objects.last())

# def rec_seed():
#     if
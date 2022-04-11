import random

from staff.forms import EmployeeForm
from staff.models import Payment, Position, Employee
from django.contrib.auth.models import User

first_names = ("Jay", "Jim", "Roy", "Axel", "Billy", "Charlie", "Jax", "Gina", "Paul",
               "Ringo", "Ally", "Nicky", "Cam", "Ari", "Trudie", "Cal", "Carl", "Lady", "Lauren",
               "Ichabod", "Arthur", "Ashley", "Drake", "Kim", "Julio", "Lorraine", "Floyd", "Janet",
               "Lydia", "Charles", "Pedro", "Bradley", "Aaron", "Abraham", "Adam", "Adrian", "Aidan",
               "Alan", "Albert", "Alejandro", "Alex", "Alexander", "Alfred", "Andrew", "Angel", "Anthony",
               "Antonio", "Ashton", "Austin", "Daniel", "David", "Dennis", "Devin", "Diego", "Dominic",
               "Donald", "Douglas", "Dylan", "Harold", "Harry", "Hayden", "Henry", "Herbert", "Horace",
               "Howard", "Hugh", "Hunter", "Malcolm", "Martin", "Mason", "Matthew", "Michael", "Miguel",
               "Miles", "Morgan")

last_names = ("Barker", "Style", "Spirits", "Murphy", "Blacker", "Bleacher", "Rogers",
              "Warren", "Keller", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis",
              "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
              "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris",
              "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young", "Allen", "Sanchez",
              "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Ramirez", "Campbell",
              "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins",
              "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy", "Rivera", "Cook", "Rogers",
              "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward",
              "Cox", "Diaz", "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James", "Reyes",
              "Cruz", "Hughes", "Price", "Myers", "Long", "Foster", "Sanders", "Ross", "Morales", "Powell",
              "Sullivan", "Russell", "Ortiz", "Jenkins", "Gutierrez", "Perry", "Butler", "Barnes", "Fisher",
              "Henderson", "Coleman", "Simmons", "Patterson", "Jordan", "Reynolds", "Hamilton", "Graham",
              "Kim", "Gonzales", "Alexander", "Ramos", "Wallace", "Griffin", "West", "Cole", "Hayes", "Chavez",
              "Gibson", "Bryant", "Ellis", "Stevens", "Murray", "Ford", "Marshall", "Owens", "McDonald", "Harrison",
              "Ruiz", "Kennedy", "Wells", "Alvarez", "Woods", "Mendoza", "Castillo", "Olson", "Webb", "Washington",
              "Tucker", "Freeman", "Burns", "Henry", "Vasquez", "Snyder", "Simpson", "Crawford", "Jimenez",
              "Porter", "Mason", "Shaw", "Gordon", "Wagner", "Hunter", "Romero", "Hicks", "Dixon", "Hunt",
              "Palmer", "Robertson", "Black", "Holmes", "Stone", "Meyer", "Boyd", "Mills", "Warren", "Fox",
              "Rose", "Rice", "Moreno", "Schmidt", "Patel", "Ferguson", "Nichols", "Herrera", "Medina", "Ryan",
              "Fernandez", "Weaver", "Daniels", "Stephens", "Gardner", "Payne", "Kelley", "Dunn", "Pierce",
              "Arnold", "Tran", "Spencer", "Peters", "Hawkins", "Grant", "Hansen", "Castro", "Hoffman", "Hart",
              "Elliott", "Cunningham", "Knight", "Bradley")

salary = (
    (15000., 14000., 17000.),
    (10000., 11000., 10500., 9500., 9700., 9200.),
    (7500., 6500., 6700., 6900., 6850., 7250., 7450., 7350., 7150., 6800.),
    (4000., 5000., 4200., 4300., 4450., 4550., 4250., 4150., 4600., 4700.),
    (2000., 3000., 2200., 2300., 2450., 2550., 2250., 2150., 2600., 2700.),
)

position = ('Ген директор', 'Старший менеджер', 'Средний менеджер', 'Рабочий', 'Младший сотрудник')

STAFF_COUNT = 25
positions_count = len(position)


def seed_full_name(first_name: tuple, last_name: tuple) -> str:
    return f'{first_name[random.randint(0, len(first_name) - 1)]} {last_name[random.randint(0, len(last_name) - 1)]}'


def seed_salary(level: int, salarys: tuple) -> float:
    return salarys[level][random.randint(0, salarys[level] - 1)]


def seed_position(level: int, positions: tuple) -> str:
    return positions[level]


def add_child(neighbor):
    print(neighbor)
    form = EmployeeForm(data={
        'name': seed_full_name(first_name=first_names, last_name=last_names),
        'parent': neighbor.id,
        'position': Position.objects.get(neighbor.position.id + 1)
    })
    if form.is_valid():
        form.safe()
    else:
        print("Data not valid")


def add_neighbor(neighbor):
    print(neighbor)
    form = EmployeeForm(data={
        'name': seed_full_name(first_name=first_names, last_name=last_names),
        'parent': neighbor.parent.id,
        'position': Position.objects.get(neighbor.position.id)
    })
    if form.is_valid():
        form.safe()
    else:
        print("Data not valid")


def add_parent(neighbor):
    print(neighbor)
    form = EmployeeForm(data={
        'name': seed_full_name(first_name=first_names, last_name=last_names),
        'parent': neighbor.parent.parent.id,
        'position': Position.objects.get(neighbor.position.id + 1)
    })
    if form.is_valid():
        form.safe()
    else:
        print("Data not valid")


if __name__ == '__main__':
    print('он начал')
    for employee_index in range(STAFF_COUNT):
        last_record = Employee.objects.last()
        if last_record is not None and 4 > last_record.level > 0:
            chance = random.randint(0, 2)
            if chance == 2:
                add_child(last_record)
            elif chance == 1:
                add_neighbor(last_record)
            else:
                add_parent(last_record)
        elif last_record is not None and last_record.level == 0:
            add_child(last_record)
        elif last_record is not None and last_record.level == 4:
            chance = random.randint(0, 1)
            if chance == 1:
                add_parent(last_record)
            else:
                add_neighbor(last_record)
        else:
            form = EmployeeForm(data={
                'name': seed_full_name(first_name=first_names, last_name=last_names),
                'parent':None,
                'position':Position.objects.get(0)
            })
            if form.is_valid():
                form.save()
            else:
                print('First employee sdox')
    print('он кончил')

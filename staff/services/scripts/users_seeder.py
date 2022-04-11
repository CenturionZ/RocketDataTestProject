from django_seed import Seed
from django.contrib.auth.models import User

seeder = Seed.seeder()

seeder.add_entity(User, 10)

seeder.execute()

from django.core.management.base import BaseCommand
from faker import Faker
from addresses.models import Address
from drivers.models import Driver
import random

class Command(BaseCommand):
    help = 'Populate the database with fake addresses and drivers'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear previous fake data (optional)
        Address.objects.all().delete()
        Driver.objects.all().delete()

        addresses = []
        for _ in range(25):
            address = Address(
                street=fake.street_address(),
                city=fake.city(),
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180),
            )
            addresses.append(address)
        Address.objects.bulk_create(addresses)
        self.stdout.write(self.style.SUCCESS(f'Created {len(addresses)} addresses.'))

        drivers = []
        for _ in range(25):
            driver = Driver(
                name=fake.name(),
                current_latitude=random.uniform(-90, 90),
                current_longitude=random.uniform(-180, 180),
                available=True,
            )
            drivers.append(driver)
        Driver.objects.bulk_create(drivers)
        self.stdout.write(self.style.SUCCESS(f'Created {len(drivers)} drivers.'))

        self.stdout.write(self.style.SUCCESS('Fake data populated successfully!'))

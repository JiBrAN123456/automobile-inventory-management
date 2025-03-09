from django.core.management.base import BaseCommand
from inventory.models import VehicleMaster
import random

class Command(BaseCommand):
    help = "Add 60 test vehicles to VehicleMaster"

    def handle(self, *args, **kwargs):
        vehicle_data = [
            {"brand": "Toyota", "model": "Camry", "year": 2022, "fuel_type": "Petrol", "transmission": "Automatic"},
            {"brand": "Honda", "model": "Civic", "year": 2023, "fuel_type": "Petrol", "transmission": "Manual"},
            {"brand": "BMW", "model": "X5", "year": 2021, "fuel_type": "Diesel", "transmission": "Automatic"},
            {"brand": "Tesla", "model": "Model 3", "year": 2024, "fuel_type": "Electric", "transmission": "Automatic"},
        ]

        # Create 60 vehicle records
        vehicles = []
        for i in range(60):
            data = random.choice(vehicle_data)
            vehicle = VehicleMaster(
                brand=data["brand"],
                model=data["model"],
                year=data["year"],
                fuel_type=data["fuel_type"],
                transmission=data["transmission"],
            )
            vehicles.append(vehicle)

        VehicleMaster.objects.bulk_create(vehicles)
        self.stdout.write(self.style.SUCCESS("✅ Successfully added 60 test vehicles!"))

from django.core.management.base import BaseCommand
from inventory.models import VehicleMaster, CompanyInventory  # ✅ Absolute import
from login.models import Company, User  # ✅ Absolute import
import random


class Command(BaseCommand):
    help = "Add 60 vehicles to Company Inventory with prices"

    def handle(self, *args, **kwargs):
        # Ensure at least one company and user exist
        company = Company.objects.first()
        user = User.objects.first()

        if not company or not user:
            self.stdout.write(self.style.ERROR("❌ No Company or User found! Create them first."))
            return

        # Sample vehicle data
        vehicles_data = [
            {"brand": "BMW", "model": "X5", "year": 2021, "fuel_type": "Diesel", "transmission": "Automatic"},
            {"brand": "Toyota", "model": "Camry", "year": 2022, "fuel_type": "Petrol", "transmission": "Automatic"},
            {"brand": "Honda", "model": "Civic", "year": 2023, "fuel_type": "Petrol", "transmission": "Manual"},
            {"brand": "Tesla", "model": "Model 3", "year": 2024, "fuel_type": "Electric", "transmission": "Automatic"},
        ]

        # ✅ Ensure master vehicles exist
        vehicle_objects = []
        for data in vehicles_data:
            vehicle, created = VehicleMaster.objects.get_or_create(
                brand=data["brand"], model=data["model"], year=data["year"],
                fuel_type=data["fuel_type"], transmission=data["transmission"]
            )
            vehicle_objects.append(vehicle)

        # ✅ Insert 60 CompanyInventory records
        inventory_objects = []
        for i in range(60):
            vehicle = random.choice(vehicle_objects)  # Pick a random vehicle
            inventory = CompanyInventory(
                company=company,
                vehicle=vehicle,
                quantity=random.randint(1, 10),  # Random quantity (1-10)
                price=random.randint(20000, 80000),  # Random price (20k-80k)
                created_by=user
            )
            inventory_objects.append(inventory)

        CompanyInventory.objects.bulk_create(inventory_objects)
        self.stdout.write(self.style.SUCCESS("✅ Successfully added 60 vehicles to Company Inventory!"))

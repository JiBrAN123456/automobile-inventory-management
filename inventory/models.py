from django.db import models
from login.models import Company , User
from django.utils.timezone import now

class VehicleMaster(models.Model):
    brand = models.CharField(max_length=100)  # e.g., Toyota, BMW
    model = models.CharField(max_length=100)  # e.g., Camry, X5
    year = models.IntegerField()  # e.g., 2022
    fuel_type = models.CharField(max_length=50, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    transmission = models.CharField(max_length=50, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    

class VehicleMasterImage(models.Model):
    vehicle = models.ForeignKey(VehicleMaster, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicle_master_images/")

    def __str__(self):
        return f"Image for {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.year})"




class CompanyInventory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory")
    vehicle = models.ForeignKey(VehicleMaster, on_delete=models.CASCADE, related_name="company_inventory")
    price = models.DecimalField(max_digits=20, decimal_places=2 , default = 500000.00)
    quantity = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.vehicle} - {self.company.name} ({self.quantity})"    
    



class CompanyInventoryImage(models.Model):
    inventory = models.ForeignKey(CompanyInventory, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="company_inventory_images/")

    def __str__(self):
        return f"Image for {self.inventory.vehicle} in {self.inventory.company.name}"



 
class VehicleDocument(models.Model):
    inventory = models.ForeignKey(CompanyInventory, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=100)  # e.g., Registration, Insurance
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return f"{self.document_type} for {self.inventory.vehicle}"

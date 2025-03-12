from django.db import models
from login.models import Company , User
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)  # e.g., "CompanyInventory"
    object_id = models.PositiveIntegerField()  # ID of the object being changed
    description = models.TextField()  # Human-readable change log
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} (ID: {self.object_id}) at {self.timestamp}"


User = get_user_model()


class AuditLogMixen(models.Model):


    def save(self,*args,**kwargs):

        is_new = self._state.adding
        super().save(*args,**kwargs)
        action = "CREATE" if is_new else "UPDATE"
        self.log_action(action)

    def delete(self,*args,**kwargs):

        self.log_action("DELETE")
        super().delete(*args,**kwargs)    

    def log_action(self,action):

        from .models import AuditLog
          
        AuditLog.objects.create(
            user=self.get_user(),
            company=self.get_company(),
            action=action,
            model_name=self.__class__.__name__,
            object_id=self.id,
            description=str(self)
        )

    def get_user(self):
        """Override this method in models to return the user making changes."""
        return None  # Needs to be set dynamically in ViewSets or Signals.

    def get_company(self):
        """Override this method in models to return the company (if applicable)."""
        return None  # Needs to be set dynamically in ViewSets or Signals.

    class Meta:
        abstract = True  # ✅ Ensure this is not created as a separate model        




class VehicleMaster(AuditLogMixen,models.Model):
    brand = models.CharField(max_length=100)  # e.g., Toyota, BMW
    model = models.CharField(max_length=100)  # e.g., Camry, X5
    year = models.IntegerField()  # e.g., 2022
    fuel_type = models.CharField(max_length=50, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    transmission = models.CharField(max_length=50, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    

class VehicleMasterImage( models.Model):
    vehicle = models.ForeignKey(VehicleMaster, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicle_master_images/")

    def __str__(self):
        return f"Image for {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.year})"




class CompanyInventory(AuditLogMixen ,models.Model):
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



 
class VehicleDocument(AuditLogMixen ,models.Model):
    inventory = models.ForeignKey(CompanyInventory, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=100)  # e.g., Registration, Insurance
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return f"{self.document_type} for {self.inventory.vehicle}"

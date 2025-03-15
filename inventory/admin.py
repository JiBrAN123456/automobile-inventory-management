from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AuditLog, VehicleMaster, CompanyInventory, VehicleDocument, VehicleMasterImage, CompanyInventoryImage

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "model_name", "object_id", "timestamp")
    list_filter = ("action", "model_name", "user")


admin.site.register(VehicleMaster)
admin.site.register(CompanyInventory)
admin.site.register(VehicleDocument)
admin.site.register(VehicleMasterImage)
admin.site.register(CompanyInventoryImage)
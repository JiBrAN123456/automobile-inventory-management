from django.contrib import admin
from .models import User, Company

# ✅ Register Company Model
admin.site.register(Company)

# ✅ Register User Model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "company", "is_staff", "is_active")  # Show in list
    search_fields = ("email",)
    list_filter = ("company", "is_active", "is_staff")

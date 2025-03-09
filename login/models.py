from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.core.exceptions import ValidationError

# ✅ Company Model
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ✅ Role Model
class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

# ✅ Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates a normal user with a required company."""
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        # ✅ Normal users **must** have a company
        if not extra_fields.get("is_superuser", False) and not extra_fields.get("company"):
            raise ValueError("Normal users must have a company.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates a superuser without requiring a company."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # ✅ Ensure `company` is not required for superusers
        extra_fields.pop("company", None)

        return self.create_user(email, password, company=None, **extra_fields)

# ✅ Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    phone_number = models.IntegerField(blank=True,null=True)
    # ✅ Allow `company` to be NULL for superusers
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL, 
        null=True,  # ✅ Allow NULL values for superusers
        blank=True,  # ✅ Allow blank values for superusers
        related_name="users",
    )

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def clean(self):
        """Ensure normal users have a company, but superusers can be without one."""
        if not self.is_superuser and self.company is None:
            raise ValidationError("Normal users must be assigned a company.")
        super().clean()


    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  
  


    def __str__(self):
        return self.user.email
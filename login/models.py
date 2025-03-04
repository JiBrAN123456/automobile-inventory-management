from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
import uuid


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Role(models.Model):
      ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

      name = models.CharField(max_length=50, choices= ROLE_CHOICES , unique=True)

      def __str__(self):
           return self.name
      
class UserManager(BaseUserManager):
      
      def create_user(self,email, password=None, **extra_fields):
           if not email:
                raise ValueError("Email is required")
           email = self.normalize_email(email)
           user = self.model(email=email , **extra_fields)
           user.set_password(password)
           user.save(using=self._db)
           return user
      
      def create_superuser(self,email, password=None , **extra_fields):
           extra_fields.setdefault('is_staff',True)
           extra_fields.setdefault('is_superuser',True)
           return self.create_user(email, password , **extra_fields)


class User(AbstractUser):
     email = models.EmailField(unique=True)
     company = models.ForeignKey(Company , on_delete=models.CASCADE , related_name='users')
     role = models.ForeignKey(Role, on_delete=models.SET_NULL , null=True , blank = True)
     

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

     objects = UserManager()

     def __str__(self):
          return self.email
     

     


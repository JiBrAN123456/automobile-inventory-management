from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a User is created."""
    if created:
        print(f"✅ Signal Triggered: Creating profile for {instance.email}")  # ✅ Debugging output
        Profile.objects.create(user=instance)

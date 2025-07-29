from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def assign_default_center(sender, instance, created, **kwargs):
    if created and not instance.center:
        # Default center assignment if missing
        from .models import Center
        default_center = Center.objects.first()
        instance.center = default_center
        instance.save()

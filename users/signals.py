from django.db.models.signals import post_save
from django.dispatch import receiver
from user_auth.models import UserRegisterToken
from .models import User

@receiver(post_save, sender=User)
def invalidate_token(sender, instance, created, **kwargs):
    if created:
        token = UserRegisterToken.objects.get(email=instance.email, is_active=True)
        token.is_active = False
        token.save()
        return token
    return False
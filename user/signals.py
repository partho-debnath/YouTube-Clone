from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import User


@receiver(post_save, sender=User)
def default_to_non_active(sender, instance, created, **kwargs):

    if created == True:
        instance.is_active = False
        instance.save()

        send_mail(
            subject = "Account Activation Link",
            message = "Goto the link and active your account",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [instance.email,]
        )
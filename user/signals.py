from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

from .models import User



@receiver(post_save, sender=User)
def default_to_non_active(sender, instance, created, **kwargs):

    if created == True:

        instance.is_active = False
        instance.save()
        
        encoded_uid = urlsafe_base64_encode(force_bytes(instance.id))
        token = PasswordResetTokenGenerator().make_token(instance)
        root_url = 'http://127.0.0.1:8000'
        url = root_url + reverse('account-activation', kwargs={'uid':encoded_uid, 'token':token})

        send_mail(
            subject = 'Account Activation Link',
            message = f'Goto the link {url} and active your account',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [instance.email,]
        )
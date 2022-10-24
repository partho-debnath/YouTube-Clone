from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


from .models import User


def get_user(kwargs)-> User:
    
    encoded_uid = kwargs['uid']
    # token = kwargs['token']
    uid = force_str(urlsafe_base64_decode(encoded_uid))
    user = get_object_or_404(User, pk=uid)
    
    return user
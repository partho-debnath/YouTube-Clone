from django.db import models

from user.models import User

# Create your models here.


class Channel(models.Model):

    user = models.OneToOneField(User, unique=True, related_name="user",
        on_delete=models.CASCADE, verbose_name='Owner')
    name = models.CharField(max_length=20, blank=False, null=False,
    verbose_name='Channel Name')
    subscriber = models.ManyToManyField(User, blank=True, null=True, 
        related_name='sususer',verbose_name='Subscriber Email')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"

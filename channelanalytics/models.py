from django.db import models
from django.core.validators import FileExtensionValidator

from user.models import User

# Create your models here.


class Channel(models.Model):

    user = models.OneToOneField(User, unique=True, related_name="user",
        on_delete=models.CASCADE, verbose_name='Owner')
    name = models.CharField(max_length=20, unique=True, blank=False, null=False,
     verbose_name='Channel Name')
    maincontent = models.FileField(help_text='Upload a Short Video.', 
        upload_to='mediafilles/', blank=True, null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    subscriber = models.ManyToManyField(User, blank=True, 
        related_name='sususer',verbose_name='Subscriber Email')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def totalSubscriber(self):
        return self.subscriber.count()
    
    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"

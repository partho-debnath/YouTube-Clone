from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

from user.models import User

# Create your models here.


class Channel(models.Model):

    user = models.OneToOneField(User, unique=True, related_name="user",
        on_delete=models.CASCADE, verbose_name='Owner')
    name = models.CharField(max_length=20, unique=True, blank=False, null=False,
     verbose_name='Channel Name')
    maincontent = models.FileField(help_text='Upload a Short Video.', 
        upload_to='mediafilles/videos/', blank=True, null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    coverPicture = models.ImageField(help_text='Upload A Cover Picture.',
        upload_to='mediafilles/coverPicture/', default='mediafilles/coverPicture/defaultCoverPicture.jpg', verbose_name='Cover Picture')
    channelLogo = models.ImageField(help_text='Upload A Picture(Channel Logo).',
        upload_to='mediafilles/logo/', default='mediafilles/logochannelLogoDefault.jpg', verbose_name='Channel Logo')
    subscriber = models.ManyToManyField(User, blank=True, 
        related_name='sususer',verbose_name='Subscriber Email')
    created = models.DateTimeField(auto_now_add=True)
    about = models.TextField(verbose_name='About This Channel.', max_length=800)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name # 2-channel-tintin

    @property
    def totalSubscriber(self):
        return self.subscriber.count()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.user.pk) + '-' + self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Channel"
        verbose_name_plural = "Channels"

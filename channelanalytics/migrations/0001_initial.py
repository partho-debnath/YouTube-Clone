# Generated by Django 4.1.1 on 2022-10-28 15:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Channel Name')),
                ('maincontent', models.FileField(blank=True, help_text='Upload a Short Video.', null=True, upload_to='mediafilles/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('coverPicture', models.ImageField(default='mediafilles/coverPicture/defaultCoverPicture.jpg', help_text='Upload A Cover Picture.', upload_to='mediafilles/coverPicture/', verbose_name='Cover Picture')),
                ('channelLogo', models.ImageField(default='mediafilles/logochannelLogoDefault.jpg', help_text='Upload A Picture(Channel Logo).', upload_to='mediafilles/logo/', verbose_name='Channel Logo')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('about', models.TextField(max_length=800, verbose_name='About This Channel.')),
                ('slug', models.SlugField(unique=True)),
                ('subscriber', models.ManyToManyField(blank=True, related_name='sususer', to=settings.AUTH_USER_MODEL, verbose_name='Subscriber Email')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
        ),
    ]

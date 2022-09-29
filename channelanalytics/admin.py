from django.contrib import admin

from . models import Channel

# Register your models here.

@admin.register(Channel)
class AdminChannel(admin.ModelAdmin):

    model = Channel
    list_display = ['user', 'name', 'created']
    list_filter = ['name', ]
    
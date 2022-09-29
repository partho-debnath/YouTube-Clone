import imp
from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.CreateChannel.as_view(), name='channel')
]
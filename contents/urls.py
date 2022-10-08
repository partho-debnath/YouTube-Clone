from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.VideoContents.as_view(), name='list'),
]
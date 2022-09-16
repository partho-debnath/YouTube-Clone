from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.Signup.as_view(), name='sign-up'),
]
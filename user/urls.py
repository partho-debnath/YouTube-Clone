from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.Signup.as_view(), name='sign-up'),
    path('account-activation/<str:uid>/<str:token>/', views.accountActivation, name='account-activation')
]
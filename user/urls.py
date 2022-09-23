from django.urls import path

from . import views


urlpatterns = [
    path('', views.Signin.as_view(), name='signin'),
    path('logout/', views.Logout, name='logout'),
    path('sign-up/', views.Signup.as_view(), name='sign-up'),
    path('change-password/', views.PasswordChange.as_view(), name='password-change'),
    path('password-reset/', views.PasswordReset.as_view(), name='password-reset'),
    path('account-activation/<str:uid>/<str:token>/', views.accountActivation, name='account-activation'),
    path('setpassword/<str:uid>/<str:token>/', views.PasswordResetConfirm.as_view(), name='confirm-password'),
    
]
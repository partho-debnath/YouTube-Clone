from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.VideoContents.as_view(), name='video-list'),
    path('<str:slug>/', views.SpecificVideoContent.as_view(), name='video-details'),
]
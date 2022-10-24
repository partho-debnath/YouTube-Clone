from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.CreateChannel.as_view(), name='create-channel'),
    path('all/', views.Channels.as_view(), name='all-channels'),
    path('<int:pk>/', views.ChannelDetails.as_view(), name='channel-details'),
    path('update-channel/<int:pk>/', views.EditChannel.as_view(), name='update-channel'),
]
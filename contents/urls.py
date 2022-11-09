from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.VideoContents.as_view(), name='video-list'),
    path('<int:pk>/', views.SpecificVideoContent.as_view(), name='play-video'),
    path('channel-subscribe/<str:slug>/', views.ChannelSubscribeOrUnsubscribe.as_view(), name='channel-un-subscribe'),
    path('like-or-remove-like-video/', views.VideoLikeOrRemoveLike.as_view(), name='video-like-or-remove-like')
]
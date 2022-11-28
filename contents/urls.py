from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.VideoContents.as_view(), name='video-list'),
    path('<int:pk>/', views.SpecificVideoContent.as_view(), name='play-video'),
    path('video-history/', views.UserVideoHistory.as_view(), name='user-video-history'),
    path('delete-all-video-history/', views.RemoveUserVideoHistory.as_view(), name='remove-user-video-history'),
    path('remove-specifi-video-history/<int:pk>/', views.RemoveUserSpecificVideoHistory.as_view(), name='remove-user-specific-video-history'),
    path('channel-subscribe/<str:slug>/', views.ChannelSubscribeOrUnsubscribe.as_view(), name='channel-un-subscribe'),
    path('like-or-remove-like-video/', views.VideoLikeOrRemoveLike.as_view(), name='video-like-or-remove-like'),
    path('add-to-watch-later/', views.AddToWatchLater.as_view(), name='add-to-watch-later')
]
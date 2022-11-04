from django.urls import path

from . import consumers

websocket_urlpatterns = [ 
    path('ws/ac/channel-subscribe/<str:channelID>/', consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]
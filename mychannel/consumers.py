from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async

import json
from user.models import User
from channelanalytics.models import Channel


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        
        subscribe = self.scope["user"]
        channelID = json.loads(self.scope['url_route']['kwargs']['channelID'])

        user = await database_sync_to_async(User.objects.get)(email=subscribe)
        channel = await database_sync_to_async(Channel.objects.get)(slug=channelID)

        try:
            unSuscChannel = await database_sync_to_async(Channel.objects.get)(slug=channelID, subscriber__email=user)
        except channel.DoesNotExist:
            await database_sync_to_async(channel.subscriber.add)(user)
            await database_sync_to_async(channel.save)()
            print('Add Subscriber')
        else:
            await database_sync_to_async(unSuscChannel.subscriber.remove)(user)
            print('Remove Subscriber')
        
        await self.accept()
        await self.disconnect(0)



class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        
        subscribe = self.scope["user"]
        channelID = json.loads(self.scope['url_route']['kwargs']['channelID'])

        user = User.objects.get(email=subscribe)
        channel = Channel.objects.get(slug=channelID)
        

        try:
            Channel.objects.get(subscriber=user.id, slug=channelID)
        except Channel.DoesNotExist:
            print('Channel Does not exist.')

        if Channel.objects.filter(subscriber=user.id, slug=channelID):
            print('exist-1')
        else:
            print('NO-1')

        if channel.subscriber.filter(user=user.id).exists() == True:
            print('exist-2')
        else:
            print('NO-2')

        channel.subscriber.add(user)
        
        channel.save()

        self.accept()
        self.disconnect(0)
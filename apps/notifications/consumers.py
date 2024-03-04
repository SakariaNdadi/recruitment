from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        print("Channel Name: ",self.channel_name)
        self.GROUP_NAME = "user-notifications"
        
        # Join channel to group
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
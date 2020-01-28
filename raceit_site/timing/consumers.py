import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class LiveDisplayConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)

    # Send message to WebSocket
    def send_result(self, event):
        self.send(text_data=json.dumps(event))

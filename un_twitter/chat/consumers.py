import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import TestMsg, Dialogue


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        text = data['text']
        dialogue = data['chat']

        await self.save_message(text, dialogue)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': text,
            }
        )

    async def chat_message(self, event):
        text = event['text']

        await self.send(text_data=json.dumps({
            'text': text,
        }))

    @sync_to_async
    def save_message(self, out_text, dialogue_num):
        d =Dialogue.objects.get(pk=dialogue_num)

        TestMsg.objects.create(dialogue=d, text=out_text)
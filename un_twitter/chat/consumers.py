import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Dialogue, Message
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from custom_users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'

        self.current_user = self.scope['user']

        red_flag = await self.check_user(self.current_user, self.room_name)
        if not red_flag:
            await self.close

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code=None):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        text = data['text']
        dialogue = data['chat']
        author = data['author']
        date_time = timezone.localtime(timezone.now())
        date = timezone.localtime(date_time).strftime('%d %b %Y')
        time = timezone.localtime(date_time).strftime('%H:%M')
        author_name = await self.get_author_name(author)

        await self.save_message(date_time, text, self.current_user, dialogue)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': text,
                'author': author,
                'date': date,
                'time': time,
                'author_name': author_name,
            }
        )

    async def chat_message(self, event):
        text = event['text']
        author = event['author']
        date = event['date']
        time = event['time']
        author_name = event['author_name']

        await self.send(text_data=json.dumps({
            'text': text,
            'author': author,
            'date': date,
            'time': time,
            'author_name': author_name
        }))

    @sync_to_async
    def save_message(self, date_time, text, author, dialogue):
        try:
            d = Dialogue.objects.get(pk=dialogue)
            user = CustomUser.objects.get(pk=author.pk)

            if len(text) <= 255:
                Message.objects.create(author=user, dialogue=d, text=text, date=date_time)
                d.last_activity = timezone.localtime(timezone.now())
                d.save()

        except ObjectDoesNotExist:
            pass

    @sync_to_async
    def check_user(self, user, dialogue):
        try:
            d_list1 = Dialogue.objects.get(side_a=user, pk=dialogue)
        except ObjectDoesNotExist:
            d_list1 = None
        try:
            d_list2 = Dialogue.objects.get(side_b=user, pk=dialogue)
        except ObjectDoesNotExist:
            d_list2 = None
        if d_list2 or d_list1:
            return True
        return False

    @sync_to_async
    def get_author_name(self, author_pk):
        try:
            user = CustomUser.objects.get(pk=author_pk)
            name = user.nickname
        except ObjectDoesNotExist:
            name = ''
        return name
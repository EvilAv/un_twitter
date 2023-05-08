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

        print(data)

        type = data['type']
        if type == 'send-msg':
            text = data['text']
            dialogue = data['chat']
            date_time = timezone.localtime(timezone.now())
            date = timezone.localtime(date_time).strftime('%d %b %Y')
            time = timezone.localtime(date_time).strftime('%H:%M')
            author_name = self.current_user.nickname

            m_id = await self.save_message(date_time, text, self.current_user, dialogue)
            if m_id:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'text': text,
                        'author': self.current_user.pk,
                        'date': date,
                        'time': time,
                        'author_name': author_name,
                        'pk': m_id,
                    }
                )
        elif type == 'read-all':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_all',
                    'author': self.current_user.pk, # we still know who sent the message to server here
                }
            )
        elif type == 'read-one':
            pk = data['id']
            if await self.mark_as_read(pk):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'read_one',
                        'pk': pk,
                    }
                )
        elif type == 'delete-one':
            pk = data['id']
            if await self.delete_message(pk, self.current_user):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'delete_one',
                        'pk': pk,
                    }
                )

    async def chat_message(self, event):
        text = event['text']
        author = event['author']
        date = event['date']
        time = event['time']
        author_name = event['author_name']
        pk = event['pk']

        await self.send(text_data=json.dumps({
            'type': 'msg-send',
            'text': text,
            'author': author,
            'date': date,
            'time': time,
            'author_name': author_name,
            'pk': pk,
        }))

    @sync_to_async
    def save_message(self, date_time, text, author, dialogue):
        try:
            d = Dialogue.objects.get(pk=dialogue)
            user = CustomUser.objects.get(pk=author.pk)

            if len(text) <= 255:
                m = Message.objects.create(author=user, dialogue=d, text=text, date=date_time)
                return m.pk

        except ObjectDoesNotExist:
            return None

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

    async def read_all(self, event):
        author = event['author']
        await self.send(text_data=json.dumps({
            'type': 'read-all',
            'author': author,
        }))

    async def read_one(self, event):
        pk = event['pk']
        await self.send(text_data=json.dumps({
            'type': 'read-one',
            'pk': pk,
        }))

    @sync_to_async
    def mark_as_read(self, pk):
        try:
            m = Message.objects.get(pk=pk)
            m.mark_as_read()
            return True
        except ObjectDoesNotExist:
            return False

    @sync_to_async
    def delete_message(self, pk, user):
        try:
            msg = Message.objects.get(pk=pk)
            if msg.author == user:
                msg.delete()
                return True
            return False
        except ObjectDoesNotExist:
            return False

    async def delete_one(self, event):
        pk = event['pk']
        await self.send(text_data=json.dumps({
            'type': 'delete-one',
            'pk': pk,
        }))


class GlobalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user = self.scope['user']
        self.room_group_name = 'global'

        print('welcome to global')
        count = await self.load_count(self.current_user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_count',
                'count': count,
                'user': self.current_user.pk,
            }
        )

    async def disconnect(self, code=None):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # inside receive we know who sent message, inside magic function we know only the user who will get message
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        chat = data['chat']
        user = await self.find_user(chat)
        if user:
            count = await self.load_count(user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_count',
                    'count': count,
                    'user': user,
                }
            )

    @sync_to_async
    def load_count(self, user):
        d_count = Dialogue.objects.filter(side_a=user, is_read_by_side_a=False).count()
        d_count += Dialogue.objects.filter(side_b=user, is_read_by_side_b=False).count()
        return d_count

    @sync_to_async
    def find_user(self, chat):
        try:
            dialogue = Dialogue.objects.get(pk=chat)
            if dialogue.side_a == self.current_user:
                return dialogue.side_b.pk
            else:
                return dialogue.side_a.pk
        except ObjectDoesNotExist:
            return None

    async def send_count(self, event):
        user = event['user']
        count = event['count']
        # print('send to '+str(self.current_user))
        if self.current_user.pk == user:
            await self.send(text_data=json.dumps({
                'count': count,
            }))

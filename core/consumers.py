import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Token authentication
        Token = apps.get_model('authtoken', 'Token')
        token_key = self.scope['query_string'].decode('utf-8').split('=')[-1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            await self.close(code=403)
            return

        # Check if user is authenticated and is a manager
        if user.is_authenticated and hasattr(user, 'employee') and user.employee.role == 'MANAGER':
            self.group_name = f"notifications_{user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=403)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))

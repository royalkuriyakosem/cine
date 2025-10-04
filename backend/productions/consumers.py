import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductionDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.production_id = self.scope['url_route']['kwargs']['production_id']
        self.group_name = f'production_{self.production_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
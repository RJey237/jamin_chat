import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .serializers  import chats_to_json
from .models import Chat, Message
class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        user=self.scope['user']

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if not user.is_authenticated:
            await self.send(json.dumps({"message":"You are not authenticated","error":403}))
            await self.disconnect()

    async def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        ) 

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action=text_data_json.get('action',None)
        if action:
            if action in self.actions:

                return await self.actions[action](self,text_data_json)
            else:
                return self.send(json.dumps({"message":"action not found","error":404}))
        else: 
            return self.send(json.dumps({"message":"invalid value","error":400}))

    # Receive message from room group
    async def chat_message(self, event):

        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


    async def fetch_chats(self,data):

        user = self.scope['user']
        chats=Chat.objects.filter(users=user)
        data =await chats_to_json(chats)

        return await self.send(json.dumps({"message":"fetch_chats","message":data}))
    
    async def fetch_messages(self,data):
        return await self.send(json.dumps({"message":"fetch_messagesd"}))
    
    async def new_messages(self,data):
        return await self.send(json.dumps({"message":"new_messages"}))

        
    actions={
        "fetch_chats":fetch_chats,
        "fetch_messages":fetch_messages,
        "new_messages":new_messages,

    }


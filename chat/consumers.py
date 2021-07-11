from django.conf import settings
import channels
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asgiref
from .exceptions import ClientError
from .utils import get_room_or_error
from channels.db import database_sync_to_async
from .models import Message

import json



class ChatConsumer(AsyncJsonWebsocketConsumer):
   
    #@database_sync_to_async
    async def fetch_message(self,room):
        print("fetch man!")
        o = Message.last_10_messsages(room)
        messages = o
        for c in messages:
            print(c.content)
        command ='fetch'
        for x in messages:
            await self.send_room(room,x.content,x.author,command)


    def new_message(self,data):
        print("newie")
        pass



   

    async def connect(self):
        
      

        if self.scope["user"].is_anonymous:
           
            await self.close()
        else:
            
            await self.accept()
            print(self.scope["subprotocols"])

       
        self.rooms = set()
        print(self.rooms,"connection done!")









    async def receive_json(self, content):
       
        
        command = content.get("command", None)
        print(content)
        print("content is ...", content)
        print(command)
        try:
            if command == "join":
                # Make them join the room
                await self.join_room(content["room"])
            elif command == "leave":
                # Leave the room
                await self.leave_room(content["room"])
            elif command == "send":
                await self.send_room(content["room"], content["message"])

            elif command == "fetch_message":
                print("enter!")
                await self.fetch_message(content["room"])
                pass
            elif command == "new_message":
                print("new_message")
                await self.new_message(content["room"])
                pass

        except ClientError as e:
            await self.send_json({"error": e.code})




    async def disconnect(self, code):
       
        print("closed man!!")
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass



    async def join_room(self, room_id):
       
        room = await get_room_or_error(room_id, self.scope["user"])
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        self.rooms.add(room_id)
        print(self.rooms)
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        await self.send_json({
            "join": str(room.id),
            "title": room.title,
        })






    async def leave_room(self, room_id):
       
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        # Remove that we're in the room
        self.rooms.discard(room_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })


    async def send_room(self, room_id, message,author=None,command=None):
        
        # Check they are in this room

        print(self.rooms)
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")
        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"])
        if command =='fetch':
            authname =str(author)
        else:
            authname =self.scope['user'].username
            print("Create message!")
            o = Message.objects.create(roomid=room_id,author=self.scope["user"],content=message)
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": authname,
                "message": message,
            }
        )




    ##### Handlers for messages sent over the channel layer












    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )













    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )










    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print(event)
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )


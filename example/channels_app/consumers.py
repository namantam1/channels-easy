from channels_easy.generic import AsyncWebsocketConsumer


class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # join room on connect
        await self.join("room1")
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room on disconnect
        await self.leave("room1")

    async def on_message(self, data):
        print("message from client", data)
        await self.emit("message", "room1", {"message": "hello from server"})

import pytest
from channels.testing import WebsocketCommunicator

from channels_easy import __version__
from channels_easy.generic import AsyncWebsocketConsumer


def test_version():
    assert __version__ == "0.3.0"


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_async_websocket_consumer():
    results = {}
    room = "room1"
    text_data = '{"type": "message", "data": "hello"}'

    class TestAsyncConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            results["connected"] = True
            await self.join(room)
            await self.accept()

        async def on_message(self, data):
            results["received"] = data
            await self.emit("message", data, room)

        async def disconnect(self, code):
            await self.leave(room)
            results["disconnected"] = code

    app = TestAsyncConsumer()

    # Test connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in results
    # Test sending Text
    await communicator.send_to(text_data=text_data)
    response = await communicator.receive_from()
    assert response == text_data
    assert results["received"] == "hello"
    # Test close
    await communicator.disconnect()
    assert "disconnected" in results


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_multiple_async_websocket_consumer():
    results = {}
    room = ["room1", "room2"]
    text_data = '{"type": "message", "data": "hello"}'

    class TestAsyncConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            results["connected"] = True
            await self.join(room)
            await self.accept()

        async def on_message(self, data):
            results["received"] = data
            await self.emit("message", data, room)

        async def disconnect(self, code):
            await self.leave(room)
            results["disconnected"] = code

    app = TestAsyncConsumer()

    # Test connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in results
    # Test sending Text
    await communicator.send_to(text_data=text_data)
    response = await communicator.receive_from()
    assert response == text_data
    assert results["received"] == "hello"
    # Test close
    await communicator.disconnect()
    assert "disconnected" in results


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_error_async_websocket_consumer():
    results = {}
    message = '{"type": "message", "data": "hello"}'

    class TestAsyncConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            results["connected"] = True
            await self.join("room1")
            await self.accept()

        async def on_message(self, data):
            results["received"] = data
            await self.emit_error("some error!", close=True)

        async def disconnect(self, code):
            results["disconnected"] = True

    app = TestAsyncConsumer()

    # Test connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in results
    # Test sending Text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    assert results["received"] == "hello"
    # Test close with error message
    assert response == '{"type": "error", "data": "some error!"}'
    await communicator.disconnect()
    assert "disconnected" in results

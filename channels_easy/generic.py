from typing import Any, Iterable, Union
from channels.generic.websocket import AsyncWebsocketConsumer as BaseConsumer

from . import json

from logging import Logger

logger = Logger(__name__)


def get_handler_name(handler_name):
    """
    Looks at a message, checks it has a sensible type, and returns the
    handler name for that type.
    """
    if handler_name.startswith("_"):
        return
    return "on_%s" % handler_name


class AsyncWebsocketConsumer(BaseConsumer):
    async def join(self, room: Union[str, Iterable]):
        """Join room with passed name

        Args:
            room (Union[str, Iterable]): List of room or a single room
        """
        if isinstance(room, str):
            rooms = [room]
        for _room in rooms:
            await self.channel_layer.group_add(_room, self.channel_name)

    async def leave(self, room: Union[str, Iterable]):
        """Leave room with passed name

        Args:
            room (Union[str, Iterable]): List of room or a single room
        """
        if isinstance(room, str):
            rooms = [room]
        for _room in rooms:
            await self.channel_layer.group_discard(_room, self.channel_name)

    async def receive(self, text_data):
        """
        Receive message from client a call the specific event
        """
        json_data = json.loads(text_data)
        if isinstance(json_data, dict) and "type" in json_data:
            handler_name = get_handler_name(json_data["type"])
            handler = getattr(self, handler_name, None)
            if handler:
                await handler(json_data["data"])
            else:
                logger.warning("%s event is not handled", handler_name)
        else:
            logger.warning("Event without type recieved from client")

    async def emit(self, typ: str, to: Union[str, Iterable], data: Any):
        """Send message to given rooms

        Args:
            typ (str): message type
            to (Union[str, Iterable]): List of rooms or a single room
            data (Any): data which is json serializable
        """
        if not isinstance(to, (list, tuple, set)):
            to = [to]
        # send to each channels
        for group in set(to):
            await self.channel_layer.group_send(
                group,
                {
                    "type": "send_message",
                    "message": {"type": typ, "data": data},
                },
            )

    async def send_message(self, event):
        """
        Send message to client
        """
        # send a message down to client
        await self.send(json.dumps(event["message"]))

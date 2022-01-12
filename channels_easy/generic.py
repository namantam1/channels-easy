from logging import Logger
from typing import Iterable, Union

from channels.generic.websocket import AsyncWebsocketConsumer as BaseConsumer

from . import json

logger = Logger(__name__)


def get_handler_name(typ):
    """
    Returns the handler name from type.
    """
    return "on_%s" % typ


class AsyncWebsocketConsumer(BaseConsumer):
    async def close_with_error(self, error_data, code=None):
        """Close socket after emitting error message

        Args:
            error_data (Any): Any json serializable data
            code (int): Close code pass to close
        """
        await self.emit_error(error_data)
        await self.close(code)

    async def emit(self, typ: str, to: Union[str, int, Iterable], data):
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
                str(group),
                {
                    "type": "send_message",
                    "message": {"type": typ, "data": data},
                },
            )

    async def emit_error(self, data):
        """Emit message with `error` type and data

        Args:
            data (Any): Any json serializable value
        """
        await self.send(
            json.dumps(
                dict(
                    type="error",
                    data=data,
                )
            )
        )

    async def join(self, room: Union[str, int, Iterable]):
        """Join room with passed name

        Args:
            room (Union[str, Iterable]): List of room or a single room
        """
        assert self.channel_layer is not None, (
            "It looks like you have not specified"
            " `CHANNEL_LAYERS` in your `settings.py`"
        )

        if isinstance(room, (str, int)):
            rooms = [room]
        else:
            rooms = room
        for _room in rooms:
            await self.channel_layer.group_add(str(_room), self.channel_name)

    async def leave(self, room: Union[str, int, Iterable]):
        """Leave room with passed name

        Args:
            room (Union[str, Iterable]): List of room or a single room
        """
        assert self.channel_layer is not None, (
            "It looks like you have not specified"
            " `CHANNEL_LAYERS` in your `settings.py`"
        )

        if isinstance(room, (str, int)):
            rooms = [room]
        else:
            rooms = room
        for _room in rooms:
            await self.channel_layer.group_discard(str(_room), self.channel_name)

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
            else:  # pragma: no cover
                logger.warning("%s event is not handled", handler_name)
        else:  # pragma: no cover
            logger.warning("Event without type recieved from client")

    async def send_message(self, event):
        """
        Send message to client
        """
        # send a message down to client
        await self.send(json.dumps(event["message"]))

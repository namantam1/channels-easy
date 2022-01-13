from logging import Logger
from typing import Iterable, Union
from xmlrpc.client import boolean

from channels.generic.websocket import AsyncWebsocketConsumer as BaseConsumer

from . import json

logger = Logger(__name__)


def get_handler_name(typ):
    """
    Returns the handler name from type.
    """
    return "on_%s" % typ


class AsyncWebsocketConsumer(BaseConsumer):
    async def emit(
        self,
        typ: str,
        data,
        to: Union[str, int, Iterable] = None,
        close: Union[int, boolean] = None,
    ):
        """Send message to given rooms

        Args:
            typ (str): message type
            data (Any): data which is json serializable
            to (Union[str, int, Iterable], optional): List of rooms or a single room
            close (Union[int, boolean], optional): Boolean or error code, If passed \
                close socket after emitting message

        *Note*: If `to` is not passed, emit message to self user
        """
        text_data = json.dumps({"type": typ, "data": data})

        if to is None:
            await self.send(text_data=text_data)
        else:
            if not isinstance(to, (list, tuple, set)):
                to = [to]
            # send to each group
            for group in set(to):
                await self.channel_layer.group_send(
                    str(group),
                    {
                        "type": "send_message",
                        "text_data": text_data,
                    },
                )

        if close is not None:
            if isinstance(close, boolean):
                await self.close()
            else:
                await self.close(close)

    async def emit_error(self, data, close: Union[int, boolean] = None):
        """Emit message with `error` type and data

        Args:
            data (Any): Any json serializable value
            close (Union[int, boolean], optional): Boolean or error code. If passed \
                close socket after emitting error
        """
        await self.emit("error", data, close=close)

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
        Send message down to Websocket
        """
        await self.send(text_data=event["text_data"])

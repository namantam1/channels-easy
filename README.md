[![codecov](https://codecov.io/gh/namantam1/channels-easy/branch/main/graph/badge.svg?token=QGazPv0Bcj)](https://codecov.io/gh/namantam1/channels-easy)
[![Release](https://github.com/namantam1/channels-easy/actions/workflows/release.yaml/badge.svg)](https://github.com/namantam1/channels-easy/actions/workflows/release.yaml)
[![Test](https://github.com/namantam1/channels-easy/actions/workflows/python-package.yml/badge.svg)](https://github.com/namantam1/channels-easy/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Channels Easy <!-- omit in toc -->
A thin wrapper around channel consumers to make things **EASY**

***Note***: This library currently support only text data which is JSON serializable.

**What problem does this library solve?**
This library simplifies two tasks for now
1. Parse incoming text data as JSON and vice versa.
2. Generate event on the basis of type passed from client side.

**Table of Contents**
- [Installation](#installation)
- [Example](#example)
- [API Usage](#api-usage)
- [Contribute](#contribute)

## Installation

To get the latest stable release from PyPi

```bash
pip install channels-easy
```
To get the latest commit from GitHub

```bash
pip install -e git+git://github.com/namantam1/channels-easy.git#egg=channels-easy
```

As `channels-easy` is a thin wrapper around `channels` so channels must be in your `INSTALLED_APPS` in `settings.py`.

```bash
INSTALLED_APPS = (
    ...,
    'channels',
)
```

## Example

All the naming convention used to implement this library is inspired from [socket.io](https://socket.io/) to make server implementation simple.

Get full example project [here](./example).

**Server side**
```python
# consumers.py
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
        # output:
        # message from client {'text': 'hello'}

        await self.emit("message", "room1", {"message": "hello from server"})

```

**Client side**

```javascript
// client.js
const socket = new WebSocket("ws://localhost:8000/ws/test/");

socket.onmessage = function ({ data }) {
    const parsed_data = JSON.parse(data);
    console.log(parsed_data);
    // output:
    // {
    //     data: {message: 'hello from server'}
    //     type: "message"
    // }
};

socket.onopen = () => {
    console.log("websocket connected...");

    // send message from client after connected
    // send with type `message` to receive from subscribed
    // `on_message` event on server side
    socket.send(
        JSON.stringify({
            type: "message",
            data: {
                text: "hello",
            },
        })
    );
};

```

## API Usage

**Subscribing to events**
We can simply subscribe to a message type as

```python
def on_<type>(self, data):
    ...
    pass
```

so if client send data as
```json
{
    "type": "message",
    "data": "Hello!"
}
```
We can subscribe to message event as

```python
def on_message(self, data):
    ...
    pass
```

**Emitting Message**

We can emit message to client using same schema that we used above

```python
def on_message(self, data):
    ...
    # some code here
    ...

    self.emit(
        "message",          # type
        ["room1"],          # room list or string
        {"text": "hello"}   # message dict | str | int | list
    )
```

Check all APIs [here](https://namantam1.github.io/channels-easy/apis/).

## Contribute

If you want to contribute to this project, please perform the following steps

```bash
# Fork this repository
# Clone your fork
poetry install

git checkout -b feature_branch master
# Implement your feature and tests
git add . && git commit
git push -u origin feature_branch
# Send us a pull request for your feature branch
```

In order to run the tests, simply execute `poetry run pytest`. This will run test created inside
`test` directory.

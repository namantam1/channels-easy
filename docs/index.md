[![codecov](https://codecov.io/gh/namantam1/channels-easy/branch/main/graph/badge.svg?token=QGazPv0Bcj)](https://codecov.io/gh/namantam1/channels-easy)
[![Release](https://github.com/namantam1/channels-easy/actions/workflows/release.yaml/badge.svg)](https://github.com/namantam1/channels-easy/actions/workflows/release.yaml)
[![Test](https://github.com/namantam1/channels-easy/actions/workflows/python-package.yml/badge.svg)](https://github.com/namantam1/channels-easy/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

channels-easy
============

A thin wrapper around channel consumers to make things **EASY**.

Installation
------------

To get the latest stable release from PyPi

```bash
pip install channels-easy
```
To get the latest commit from GitHub

```bash
pip install -e git+git://github.com/namantam1/channels-easy.git#egg=channels-easy
```
<!-- TODO: Describe further installation steps (edit / remove the examples below): -->

As `channels-easy` is a thin wrapper around `channels` so channels must be in your `INSTALLED_APPS` in `settings.py`.

```bash
INSTALLED_APPS = (
    ...,
    'channels',
)
```

Usage
-----

All the naming convention used to implement this library is inspired from [socket.io](https://socket.io/) to make server implementation simple.

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
        await self.emit("message", "room1", {"message": "hello from server"})

```

Contribute
----------

If you want to contribute to this project, please perform the following steps

````bash
# Fork this repository
# Clone your fork
poetry install

git checkout -b feature_branch master
# Implement your feature and tests
git add . && git commit
git push -u origin feature_branch
# Send us a pull request for your feature branch
````
<!-- In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments. -->

from json import *

from django.core.serializers.json import DjangoJSONEncoder

_dumps = dumps


def dumps(*args, **kwargs):
    kwargs.pop("cls", None)
    return _dumps(*args, cls=DjangoJSONEncoder, **kwargs)

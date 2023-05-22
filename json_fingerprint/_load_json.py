import json

from .exceptions import JSONLoad


def _load_json(data: str):
    try:
        return json.loads(data)
    except Exception:
        err = "Unable to load JSON"
        raise JSONLoad(err) from None

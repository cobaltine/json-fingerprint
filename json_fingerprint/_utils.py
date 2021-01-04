import json

from ._exceptions import FingerprintJSONLoadError


def _load_json(data: str):
    try:
        return json.loads(data)
    except Exception:
        err = 'Unable to load JSON'
        raise FingerprintJSONLoadError(err) from None

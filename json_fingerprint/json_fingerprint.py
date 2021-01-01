import json

from ._jfpv1 import _create_jfpv1_fingerprint
from ._validators import (
    _validate_hash_function,
    _validate_input_type,
    _validate_version,
)


class FingerprintJSONLoadError(Exception):
    pass


def json_fingerprint(input: str, hash_function: str, version: int) -> str:
    """Create json fingerprints with the selected hash function and jfp version."""
    _validate_version(version=version)
    _validate_input_type(input=input)
    _validate_hash_function(hash_function=hash_function, version=version)

    try:
        loaded = json.loads(input)
    except Exception:
        err = 'Unable to load JSON'
        raise FingerprintJSONLoadError(err) from None

    return _create_jfpv1_fingerprint(data=loaded, hash_function=hash_function, version=version)

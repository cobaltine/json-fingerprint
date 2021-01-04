from ._jfpv1 import _create_jfpv1_fingerprint
from ._utils import _load_json
from ._validators import (
    _validate_hash_function,
    _validate_input_type,
    _validate_version,
)


def json_fingerprint(input: str, hash_function: str, version: int) -> str:
    """Create json fingerprints with the selected hash function and jfp version."""
    _validate_version(version=version)
    _validate_input_type(input=input)
    _validate_hash_function(hash_function=hash_function, version=version)
    loaded = _load_json(data=input)
    return _create_jfpv1_fingerprint(data=loaded, hash_function=hash_function, version=version)

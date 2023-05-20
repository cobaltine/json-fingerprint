from ._jfpv1 import _create_jfpv1_fingerprint
from ._load_json import _load_json
from ._validators import (
    _validate_hash_function,
    _validate_input_type,
    _validate_version,
)


def create(input: str, hash_function: str, version: int) -> str:
    """Create JSON fingerprints with the selected hash function and JSON fingerprint algorithm version.

    Args:
        input (str):
            JSON input in string format.
        hash_function (str):
            One of the supported hash function names in string format (options: "sha256", "sha384", or "sha512").
        version (int):
            An integer indicating the JSON fingerprint algorithm version to be used (options: 1).

    Returns:
        str: A pre-formatted JSON fingerprint (example: "jfpv1${hash_function_name}${hash_hex_digest}").
    """
    _validate_version(version=version)
    _validate_input_type(input=input)
    _validate_hash_function(hash_function=hash_function, version=version)
    loaded = _load_json(data=input)
    return _create_jfpv1_fingerprint(data=loaded, hash_function=hash_function)

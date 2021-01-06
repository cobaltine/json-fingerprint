from typing import Tuple
from ._validators import _validate_fingerprint_format


def decode(fingerprint: str) -> Tuple[int, str, str]:
    """Decode json fingerprints into version, hash function and hash values."""
    _validate_fingerprint_format(fingerprint)
    elements = fingerprint.split('$')
    version = int(elements[0][4:])
    hash_function = elements[1]
    hash = elements[2]

    return version, hash_function, hash

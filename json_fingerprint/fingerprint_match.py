from .decode_fingerprint import decode_fingerprint
from .json_fingerprint import json_fingerprint


def fingerprint_match(input: str, target_fingerprint: str) -> bool:
    """Match raw json str input to target fingerprint.

    Decodes the target fingerprint and creates a fingerprint from the input with identical parameters."""
    version, hash_function, _ = decode_fingerprint(fingerprint=target_fingerprint)
    input_fingerprint = json_fingerprint(input=input, hash_function=hash_function, version=version)
    if input_fingerprint == target_fingerprint:
        return True
    return False

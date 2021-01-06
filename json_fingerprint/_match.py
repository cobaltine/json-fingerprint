from ._decode import decode
from ._create import create


def match(input: str, target_fingerprint: str) -> bool:
    """Match raw json str input to target fingerprint.

    Decodes the target fingerprint and creates a fingerprint from the input with identical parameters."""
    version, hash_function, _ = decode(fingerprint=target_fingerprint)
    input_fingerprint = create(input=input, hash_function=hash_function, version=version)
    if input_fingerprint == target_fingerprint:
        return True
    return False

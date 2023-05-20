from ._create import create
from ._decode import decode


def match(input: str, target_fingerprint: str) -> bool:
    """Match raw json string input to target fingerprint.

    Decodes the target fingerprint and creates a fingerprint from the input with identical parameters.
    If the target fingerprint uses, for example, the "sha256" hash function, then a JSON fingerprint
    with "sha256" is also generated prior to matching.

    Args:
        input (str):
            JSON input in string format.
        target_fingerprint (str):
            Target JSON fingerprint in string format.

    Returns:
        bool: True if the input JSON data matches with the target fingerprint, otherwise False.
    """
    version, hash_function, _ = decode(fingerprint=target_fingerprint)
    input_fingerprint = create(input=input, hash_function=hash_function, version=version)
    if input_fingerprint == target_fingerprint:
        return True
    return False

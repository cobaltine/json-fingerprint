from typing import Tuple

from ._validators import _validate_fingerprint_format


def decode(fingerprint: str) -> Tuple[int, str, str]:
    """Decode json fingerprints into version, hash function, and the hex digest of the hash value.

    Args:
        fingerprint (str):
            A valid JSON fingerprint (example: "jfpv1$sha256$2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03")

    Returns:
        A tuple containing the following items
        - int: JSON fingerprint version (example: 1)
        - str: hash function name (example: "sha256")
        - str: a hex digest of the secure hash value (example: "2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03")
    """
    _validate_fingerprint_format(fingerprint)
    elements = fingerprint.split("$")
    version = int(elements[0][4:])
    hash_function = elements[1]
    hash = elements[2]

    return version, hash_function, hash

from typing import Dict, List

from ._create import create
from ._decode import decode


def _get_target_hashes(fingerprints: List[str]) -> List[Dict]:
    target_hashes = []
    for fingerprint in fingerprints:
        version, hash_function, _ = decode(fingerprint=fingerprint)
        element = {"version": version, "hash_function": hash_function}
        if element not in target_hashes:
            target_hashes.append(element)

    return target_hashes


def _create_input_fingerprints(input: str, target_hashes: List[Dict]) -> List[str]:
    input_fingerprints = []
    for element in target_hashes:
        fingerprint = create(input=input, hash_function=element["hash_function"], version=element["version"])
        input_fingerprints.append(fingerprint)
    return input_fingerprints


def find_matches(input: str, fingerprints: List[str], deduplicate: bool = False) -> List[str]:
    """Match raw json str input to a list of fingerprints.

    Decodes the target fingerprints and creates a fingerprint from the input with identical parameters.
    Creates a fingerprint from the input of each different JSON fingerprint type present in the fingerprint list."""
    if deduplicate:
        fingerprints = list(set(fingerprints))
    target_hashes = _get_target_hashes(fingerprints=fingerprints)
    input_fingerprints = _create_input_fingerprints(input=input, target_hashes=target_hashes)

    matches = []
    for fingerprint in fingerprints:
        if fingerprint in input_fingerprints:
            matches.append(fingerprint)

    return matches

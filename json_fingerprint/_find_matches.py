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
    """Create all necessary JSON fingerprint variations of the JSON data input."""
    input_fingerprints = []
    for element in target_hashes:
        fingerprint = create(input=input, hash_function=element["hash_function"], version=element["version"])
        input_fingerprints.append(fingerprint)
    return input_fingerprints


def find_matches(input: str, fingerprints: List[str], deduplicate: bool = False) -> List[str]:
    """Match raw json string input to a list of fingerprints.

    The fingerprint matching is executed as follows:
        1. Optional: deduplicate the target fingerprint list
        2. Decode the target fingerprint list to find all different JSON fingerprint variations (hash function, version)
        3. Create JSON fingerprints from the input with identical parameters (e.g., all hash function variations)
        4. Compare the input JSON fingerprint variations to the target list and find all matches

    If there is e.g. "sha256" and "sha512" JSON fingerprint variations in the target list of fingerprints,
    then a JSON fingerprint is created from the input JSON data with both the "sha256" and the "sha512" hash functions.

    Args:
        input (str):
            JSON input in string format.
        fingerprints (list of strings):
            A list of JSON fingerprints in string format.
        deduplicate (bool):
            If True, then deduplicate the fingerprint list before processing matches. False by default.

    Returns:
        list: A list of JSON fingerprint matches in string format.
    """
    if deduplicate:
        fingerprints = list(set(fingerprints))
    target_hashes = _get_target_hashes(fingerprints=fingerprints)
    input_fingerprints = _create_input_fingerprints(input=input, target_hashes=target_hashes)

    matches = []
    for fingerprint in fingerprints:
        if fingerprint in input_fingerprints:
            matches.append(fingerprint)

    return matches

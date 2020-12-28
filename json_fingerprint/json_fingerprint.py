import hashlib
import json

from typing import (
    Dict,
    List,
)

JFPV1_HASH_FUNCTIONS = (
    'sha256',
)

JSON_FINGERPRINT_VERSIONS = (
    1,
)


class FingerprintJSONLoadError(Exception):
    pass


class FingerprintInputDataTypeError(Exception):
    pass


class FingerprintHashFunctionError(Exception):
    pass


class FingerprintVersionError(Exception):
    pass


def _create_json_sha256_hash(data) -> str:
    """Create an sha256 hash from json-converted data, sorted by key names."""
    stringified = json.dumps(data, sort_keys=True)
    m = hashlib.sha256()
    m.update(stringified.encode('utf-8'))
    return m.hexdigest()


def _create_sorted_sha256_hash_list(data: Dict) -> List[Dict]:
    """Create a sorted sha256 hash list."""
    out = []
    for obj in data:
        hash = _create_json_sha256_hash(obj)
        out.append(hash)
    out.sort()
    return out


def _build_path(key: str, base_path: str):
    if base_path:
        return f'{base_path}|{key}'
    return key


def _flatten_json(data: Dict, path: str = '', siblings: List = [], debug: bool = False) -> List:
    """Flatten json data structures into a sibling-aware data element list."""
    out = []
    if type(data) is dict:
        for key in data.keys():
            p = _build_path(key=f'{{{key}}}', base_path=path)
            output = _flatten_json(data=data[key], path=p, siblings=siblings, debug=debug)
            out.extend(output)
        return out

    if type(data) is list:
        p = _build_path(key=f'[{len(data)}]', base_path=path)
        siblings = []
        for item in data:
            output = _flatten_json(data=item, path=p, debug=debug)
            siblings.extend(output)

        for item in data:
            output = _flatten_json(data=item, path=p, siblings=siblings, debug=debug)
            out.extend(output)
        return out

    if not debug:
        siblings = _create_sorted_sha256_hash_list(siblings)
    element = {
        'path': path,
        'siblings': siblings,
        'value': data,
    }
    out.append(element)
    return out


def json_fingerprint(input: str, hash_function: str, version: str) -> str:
    """Create json fingerprints with the selected hash function and jfp version."""
    if type(input) is not str:
        err = f'Expected data type \'{type("")}\' (JSON in string format), instead got \'{type(input)}\''
        raise FingerprintInputDataTypeError(err)

    if hash_function not in JFPV1_HASH_FUNCTIONS:
        err = (f'Expected one of supported hash functions \'{JFPV1_HASH_FUNCTIONS}\', '
               f'instead got \'{hash_function}\'')
        raise FingerprintHashFunctionError(err)

    if version not in JSON_FINGERPRINT_VERSIONS:
        err = (f'Expected one of supported JSON fingerprint versions \'{JSON_FINGERPRINT_VERSIONS}\', '
               f'instead got \'{version}\'')
        raise FingerprintVersionError(err)

    try:
        loaded = json.loads(input)
    except Exception:
        err = 'Unable to load JSON'
        raise FingerprintJSONLoadError(err) from None

    flattened_json = _flatten_json(data=loaded)
    sorted_hash_list = _create_sorted_sha256_hash_list(data=flattened_json)
    hex_digest = _create_json_sha256_hash(sorted_hash_list)
    return f'jfpv1${hash_function}${hex_digest}'

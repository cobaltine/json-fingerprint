import hashlib
import json

from typing import (
    Dict,
    List,
)

FINGERPRINT_HASH_FUNCTIONS = (
    'sha256',
)

FINGERPRINT_VERSIONS = (
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


def _create_hash(data) -> str:
    stringified = json.dumps(data, sort_keys=True)
    m = hashlib.sha256()
    m.update(stringified.encode('utf-8'))
    return m.hexdigest()


def _create_sorted_hash_list(data: Dict) -> List[Dict]:
    out = []
    for obj in data:
        hash = _create_hash(obj)
        out.append(hash)
    out.sort()
    return out


def _flatten_json(data: Dict, path: str = '', siblings: List = [], debug: bool = False) -> List:
    out = []
    if type(data) is dict:
        for key in data.keys():
            p = f'{{{key}}}'
            if path:
                p = f'{path}|{p}'
            out.extend(_flatten_json(data[key], path=p, siblings=siblings, debug=debug))
    elif type(data) is list:
        p = f'[{len(data)}]'
        if path:
            p = f'{path}|{p}'

        siblings = []
        for item in data:
            output = _flatten_json(item, path=p, debug=debug)
            siblings.extend(output)

        for item in data:
            output = _flatten_json(item, path=p, siblings=siblings, debug=debug)
            out.extend(output)
    else:
        if not debug:
            siblings = _create_sorted_hash_list(siblings)
        element = {
            'path': path,
            'siblings': siblings,
            'value': data,
        }
        out.append(element)

    return out


def json_fingerprint(input: str, hash_function: str, version: str) -> str:
    if type(input) is not str:
        err = f'Expected data type \'{type("")}\' (JSON in string format), instead got \'{type(input)}\''
        raise FingerprintInputDataTypeError(err)

    if hash_function not in FINGERPRINT_HASH_FUNCTIONS:
        err = (f'Expected one of supported hash functions \'{FINGERPRINT_HASH_FUNCTIONS}\', '
               f'instead got \'{hash_function}\'')
        raise FingerprintHashFunctionError(err)

    if version not in FINGERPRINT_VERSIONS:
        err = (f'Expected one of supported JSON fingerprint versions \'{FINGERPRINT_VERSIONS}\', '
               f'instead got \'{version}\'')
        raise FingerprintVersionError(err)

    try:
        loaded = json.loads(input)
    except Exception:
        err = 'Unable to load JSON'
        raise FingerprintJSONLoadError(err) from None

    flattened_json = _flatten_json(data=loaded)
    sorted_hash_list = _create_sorted_hash_list(data=flattened_json)
    hex_digest = _create_hash(sorted_hash_list)
    return f'jfpv1${hash_function}${hex_digest}'

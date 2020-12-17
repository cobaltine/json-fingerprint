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


def _flatten_json(data: Dict, out: List, path: str = '') -> List:
    if type(data) is dict:
        for key in data.keys():
            if path:
                p = f'{path}|{{{key}}}'
            else:
                p = key
            _flatten_json(data[key], out=out, path=p)
    elif type(data) is list:
        if path:
            p = f'{path}|[{len(data)}]'
        else:
            p = f'[{len(data)}]'
        for item in data:
            _flatten_json(item, out=out, path=p)
    else:
        out.append({
            'path': path,
            'value': data
        })

    return out

def _create_hash_list(data: Dict) -> List[Dict]:
    out = []
    for obj in data:
        stringified = json.dumps(obj, sort_keys=True)
        m = hashlib.sha256()
        m.update(stringified.encode('utf-8'))
        out.append(m.hexdigest())
    out.sort()
    return out

def json_fingerprint(data: str, hash_function: str, version: str) -> str:
    if type(data) is not str:
        err = f'Expected data type \'{type("")}\' (JSON in string format), instead got \'{type(data)}\''
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
        loaded = json.loads(data)
    except Exception:
        err = 'Unable to load JSON'
        raise FingerprintJSONLoadError(err) from None

    flattened_json = []
    _flatten_json(data=loaded, out=flattened_json)
    hash_list = _create_hash_list(data=flattened_json)
    stringified = json.dumps(hash_list)
    m = hashlib.sha256()
    m.update(stringified.encode('utf-8'))
    return f'jfpv1${hash_function}${m.hexdigest()}'

import hashlib
import json

from typing import (
    Any,
    Dict,
    List,
)


def _create_json_hash(data: Any, hash_function: str) -> str:
    """Create an sha256 hash from json-converted data, sorted by key names."""
    stringified = json.dumps(
        data,
        allow_nan=False,
        ensure_ascii=False,
        indent=None,
        separators=(',', ':'),
        skipkeys=False,
        sort_keys=True,
    )
    if hash_function == 'sha256':
        m = hashlib.sha256()
    if hash_function == 'sha384':
        m = hashlib.sha384()
    if hash_function == 'sha512':
        m = hashlib.sha512()
    m.update(stringified.encode('utf-8'))

    return m.hexdigest()


def _create_sorted_hash_list(data: Dict, hash_function: str) -> List[Dict]:
    """Create a sorted sha256 hash list."""
    out = []
    for obj in data:
        hash = _create_json_hash(obj, hash_function=hash_function)
        out.append(hash)
    out.sort()
    return out


def _build_path(key: str, base_path: str):
    """Build a path string."""
    if base_path:
        return f'{base_path}|{key}'
    return key


def _build_element(path: str, siblings: str, value: Any):
    """Build an element dictionary based on presence of sibling data."""
    if siblings:
        return {
            'path': path,
            'siblings': siblings,
            'value': value,
        }

    return {
        'path': path,
        'value': value,
    }


def _flatten_json(data: Dict, hash_function: str, path: str = '', siblings: List = [], debug: bool = False) -> List:
    """Flatten json data structures into a sibling-aware data element list."""
    out = []
    if type(data) is dict:
        for key in data.keys():
            p = _build_path(key=f'{{{key}}}', base_path=path)
            output = _flatten_json(data=data[key], hash_function=hash_function, path=p, siblings=siblings, debug=debug)
            out.extend(output)
        return out

    if type(data) is list:
        p = _build_path(key=f'[{len(data)}]', base_path=path)

        # Iterate and collect sibling structures, which'll be then attached to each sibling element
        siblings = []
        for item in data:
            output = _flatten_json(data=item, hash_function=hash_function, path=p, debug=debug)
            siblings.extend(output)

        # Debug mode, which allows non-hashed sibling structures to be inspected and tested against
        if not debug:
            siblings = _create_sorted_hash_list(data=siblings, hash_function=hash_function)
            siblings = _create_json_hash(data=siblings, hash_function=hash_function)

        # Recurse with each value in list to typecheck it and eventually get the element value
        for item in data:
            output = _flatten_json(data=item, hash_function=hash_function, path=p, siblings=siblings, debug=debug)
            out.extend(output)
        return out

    element = _build_element(path=path, siblings=siblings, value=data)
    out.append(element)
    return out


def _create_jfpv1_fingerprint(data: Any, hash_function: str, version: int):
    """Create a jfpv1 fingerprint."""
    flattened_json = _flatten_json(data=data, hash_function=hash_function)
    sorted_hash_list = _create_sorted_hash_list(data=flattened_json, hash_function=hash_function)
    hex_digest = _create_json_hash(data=sorted_hash_list, hash_function=hash_function)
    return f'jfpv1${hash_function}${hex_digest}'

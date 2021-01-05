# json-fingerprint

![](https://img.shields.io/github/license/cobaltine/json-fingerprint) ![](https://img.shields.io/pypi/pyversions/json-fingerprint) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Test%20runner/main) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Release%20Python%20package/main?label=pypi%20release) [![](https://img.shields.io/pypi/v/json-fingerprint)](https://pypi.org/project/json-fingerprint/) ![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/cobaltine/json-fingerprint) [![Coverage Status](https://coveralls.io/repos/github/cobaltine/json-fingerprint/badge.svg?branch=main)](https://coveralls.io/github/cobaltine/json-fingerprint?branch=main)


Create consistent and comparable fingerprints with secure hashes from unordered JSON data.

A json fingerprint consists of three parts: the version of the underlying algorithm, the hash function used and a hex digest of the hash function output. A complete example could look like this: `jfpv1$sha256$5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af`.

The first part indicates the algorithm version, `jfpv1`, which would translate to **j**son **f**inger**p**rint **v**ersion **1**. The second part, `sha256`, indicates that SHA256 is the hash function that was used. The last part, `5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af`, is a standard hex digest of the hash function output.


<!-- TOC titleSize:2 tabSpaces:2 depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 skip:0 title:1 charForUnorderedList:* -->
## Table of Contents
* [v1 release checklist (jfpv1)](#v1-release-checklist-jfpv1)
* [Installation](#installation)
* [Examples](#examples)
  * [Creating fingerprints from JSON data](#creating-fingerprints-from-json-data)
  * [Decoding JSON fingerprints](#decoding-json-fingerprints)
  * [Fingerprint matching](#fingerprint-matching)
<!-- /TOC -->


## v1 release checklist (jfpv1)

This is a list of high-level development and documentation tasks, which need to be completed prior to freezing the API for v1. Prior to v1, backwards-incompatible changes are possible.

- [ ] Formalized the jfpv1 specification
- [x] JSON type support
  - [x] Primitives and literals
  - [x] Arrays
  - [x] Objects
- [x] Flattened "sibling-aware" internal data structure
- [x] Support nested JSON data structures with mixed types
- [x] Support most common SHA-2 hash functions
  - [x] SHA256
  - [x] SHA384
  - [x] SHA512
- [x] Dynamic jfpv1 fingerprint comparison function (JSON string against a fingerprint)
- [x] Performance characteristics that scale sufficiently
- [ ] Extensive verification against potential fingerprint (hash) collisions


## Installation

To install the json-fingerprint package, run `pip install json-fingerprint`.


## Examples

The complete working examples below show how to create and compare JSON fingerprints.


### Creating fingerprints from JSON data

Fingerprints can be created with the `json_fingerprint()` function, which requires three arguments: input (valid JSON string), hash function (`sha256`, `sha384` and `sha512` are supported) and JSON fingerprint version (`1`).

```python
import json

from json_fingerprint import json_fingerprint

obj_1_str = json.dumps([3, 2, 1, [True, False], {'foo': 'bar'}])
obj_2_str = json.dumps([2, {'foo': 'bar'}, 1, [False, True], 3])  # Same data in different order
fp_1 = json_fingerprint(input=obj_1_str, hash_function='sha256', version=1)
fp_2 = json_fingerprint(input=obj_2_str, hash_function='sha256', version=1)
print(f'Fingerprint 1: {fp_1}')
print(f'Fingerprint 2: {fp_2}')
```
This will output two identical fingerprints regardless of the different order of the json elements:

```
Fingerprint 1: jfpv1$sha256$164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a
Fingerprint 2: jfpv1$sha256$164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a
```

Since json objects with identical data content and structure will always produce identical fingerprints, the fingerprints can be used effectively for various purposes. These include finding duplicate json data from a larger dataset, json data cache validation/invalidation and data integrity checking.


### Decoding JSON fingerprints

JSON fingerprints can be decoded with the `decode_fingerprint()` convenience function, which returns the version, hash function and hash in a tuple.

```python
from json_fingerprint import decode_fingerprint

fingerprint = 'jfpv1$sha256$164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a'
version, hash_function, hash = decode_fingerprint(fingerprint=fingerprint)
print(f'Version (integer): {version}')
print(f'Hash function: {hash_function}')
print(f'Hash: {hash}')
```
This will output the individual elements that make up a fingerprint as follows:

```
Version (integer): 1
Hash function: sha256
Hash: 164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a
```


### Fingerprint matching

The `fingerprint_match()` is another convenience function that matches JSON data against a fingerprint, and returns either `True` or `False` depending on whether the data matches the fingerprint or not. Internally, it will automatically choose the correct version and hash function based on the `target_fingerprint` argument.

```python
import json

from json_fingerprint import fingerprint_match

input_1 = json.dumps([3, 2, 1, [True, False], {'foo': 'bar'}])
input_2 = json.dumps([3, 2, 1])
target_fingerprint = 'jfpv1$sha256$164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a'
match_1 = fingerprint_match(input=input_1, target_fingerprint=target_fingerprint)
match_2 = fingerprint_match(input=input_2, target_fingerprint=target_fingerprint)
print(f'Fingerprint matches with input_1: {match_1}')
print(f'Fingerprint matches with input_2: {match_2}')
```
This will output the following:
```
Fingerprint matches with input_1: True
Fingerprint matches with input_2: False
```

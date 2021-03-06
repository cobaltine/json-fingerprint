# json-fingerprint

![](https://img.shields.io/github/license/cobaltine/json-fingerprint) ![](https://img.shields.io/pypi/pyversions/json-fingerprint) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Test%20runner/main?label=ci) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Release%20Python%20package/main?label=cd) [![](https://img.shields.io/pypi/v/json-fingerprint)](https://pypi.org/project/json-fingerprint/) ![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/cobaltine/json-fingerprint) [![Coverage Status](https://coveralls.io/repos/github/cobaltine/json-fingerprint/badge.svg?branch=main)](https://coveralls.io/github/cobaltine/json-fingerprint?branch=main)


Create consistent and comparable fingerprints with secure hashes from unordered JSON data.

A JSON fingerprint consists of three parts: the version of the underlying canonicalization algorithm, the hash function used and a hexadecimal digest of the hash function output. A complete example could look like this: `jfpv1$sha256$5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af`.

| Fingerprint element | Description                                                                         |
|:--------------------|:------------------------------------------------------------------------------------|
| jfpv1               | JSON fingerprint version identifier: **j**son **f**inger**p**rint **v**ersion **1** |
| sha256              | Hash function identifier (sha256, sha384 or sha512)                                 |
| 5815eb0c...1fae86af | The secure hash function output in hexadecimal format                               |


<!-- TOC titleSize:2 tabSpaces:2 depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 skip:0 title:1 charForUnorderedList:* -->
## Table of Contents
* [v1 release checklist (jfpv1)](#v1-release-checklist-jfpv1)
* [Installation](#installation)
* [Examples](#examples)
  * [Create JSON fingerprints](#create-json-fingerprints)
  * [Decode JSON fingerprints](#decode-json-fingerprints)
  * [Match fingerprints](#match-fingerprints)
  * [Find matches in fingerprint lists](#find-matches-in-fingerprint-lists)
* [JSON normalization](#json-normalization)
  * [Alternative specifications](#alternative-specifications)
  * [JSON Fingerprint v1 (jfpv1)](#json-fingerprint-v1-jfpv1)
* [Running tests](#running-tests)
<!-- /TOC -->


## v1 release checklist (jfpv1)

This is a list of high-level development and documentation tasks, which need to be completed prior to freezing the API for v1. Before v1, backwards-incompatible changes to the API are possible, although not likely from v0.10.0 onwards. Since the jfpv1 spec is work in progress, the fingerprints may not be fully comparable between different _0.y.z_ versions.

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

The complete working examples below show how to use all core features of the `json_fingerprint` package.


### Create JSON fingerprints

JSON fingerprints can be created with the `create()` function, which requires three arguments: input (valid JSON string), hash function (SHA256, SHA384 and SHA512 are supported) and JSON fingerprint version (1).

```python
import json
import json_fingerprint

input_1 = json.dumps([3, 2, 1, [True, False], {'foo': 'bar'}])
input_2 = json.dumps([2, {'foo': 'bar'}, 1, [False, True], 3])  # Different order
fp_1 = json_fingerprint.create(input=input_1, hash_function='sha256', version=1)
fp_2 = json_fingerprint.create(input=input_2, hash_function='sha256', version=1)
print(f'Fingerpr. 1: {fp_1}')
print(f'Fingerpr. 2: {fp_2}')
```
This will output two identical fingerprints regardless of the different order of the json elements:

```
Fingerpr. 1: jfpv1$sha256$2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03
Fingerpr. 2: jfpv1$sha256$2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03
```

Since JSON objects with identical data content and structure will always produce identical fingerprints, the fingerprints can be used effectively for various purposes. These include finding duplicate JSON data from a larger dataset, JSON data cache validation/invalidation and data integrity checking.


### Decode JSON fingerprints

JSON fingerprints can be decoded with the `decode()` convenience function. It returns the version, hash function and secure hash in a tuple.

```python
import json_fingerprint

fp = 'jfpv1$sha256$2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03'
version, hash_function, hash = json_fingerprint.decode(fingerprint=fp)
print(f'Version (integer): {version}')
print(f'Hash function: {hash_function}')
print(f'Secure hash: {hash}')
```
This will output the individual elements that make up a fingerprint as follows:

```
Version (integer): 1
Hash function: sha256
Secure hash: 164e2e93056b7a0e4ace25b3c9aed9cf061f9a23c48c3d88a655819ac452b83a
```


### Match fingerprints

The `match()` is another convenience function that matches JSON data against a fingerprint, and returns either `True` or `False` depending on whether the data matches the fingerprint or not. Internally, it will automatically choose the correct version and hash function based on the `target_fingerprint` argument.

```python
import json
import json_fingerprint

input_1 = json.dumps([3, 2, 1, [True, False], {'foo': 'bar'}])
input_2 = json.dumps([3, 2, 1])
target_fp = 'jfpv1$sha256$2ecb0c919fcb06024f55380134da3bbaac3879f98adce89a8871706fe50dda03'
match_1 = json_fingerprint.match(input=input_1, target_fingerprint=target_fp)
match_2 = json_fingerprint.match(input=input_2, target_fingerprint=target_fp)
print(f'Fingerprint matches with input_1: {match_1}')
print(f'Fingerprint matches with input_2: {match_2}')
```
This will output the following:
```
Fingerprint matches with input_1: True
Fingerprint matches with input_2: False
```


### Find matches in fingerprint lists

The `find_matches()` function takes a JSON string and a list of JSON fingerprints as input. It creates a fingerprint of the JSON input string of each different variant in the target list, and looks for matches in the fingerprint list. It can optionally also deduplicate the fingerprint input list, and results list.

```python
import json
import json_fingerprint

# Produces SHA256: jfpv1$sha256$d119f4d8...b1710d9f
# Produces SHA384: jfpv1$sha384$9bca46fd...fd0e2e9c
input = json.dumps({'foo': 'bar'})
fingerprints = [
    # SHA256 match
    'jfpv1$sha256$d119f4d8b802091520162b78f57a995a9ecbc88b20573b0c7e474072b1710d9f',
    # SHA256 match (duplicate)
    'jfpv1$sha256$d119f4d8b802091520162b78f57a995a9ecbc88b20573b0c7e474072b1710d9f',
    # SHA384 match
    ('jfpv1$sha384$9bca46fd7ef7aa2e16e68978b5eb5c294bd5b380780e81bcb1af97d4b339bca'
     'f7f6a622b2f1a955eea2fadb8fd0e2e9c'),
    # SHA256, not a match
    'jfpv1$sha256$73f7bb145f268c033ec22a0b74296cdbab1405415a3d64a1c79223aa9a9f7643',
]
matches = json_fingerprint.find_matches(input=input, fingerprints=fingerprints)
# Print raw matches, which include 2 same SHA256 fingerprints
print(*(f'\nMatch: {match[0:30]}...' for match in matches))
deduplicated_matches = json_fingerprint.find_matches(input=input,
                                                     fingerprints=fingerprints,
                                                     deduplicate=True)
# Print deduplicated matches
print(*(f'\nDeduplicated match: {match[0:30]}...' for match in deduplicated_matches))
```
This will output the following results, first the list with a duplicate and the latter with deduplicated results:
```
Match: jfpv1$sha256$d119f4d8b80209152...
Match: jfpv1$sha256$d119f4d8b80209152...
Match: jfpv1$sha384$9bca46fd7ef7aa2e1...

Deduplicated match: jfpv1$sha384$9bca46fd7ef7aa2e1...
Deduplicated match: jfpv1$sha256$d119f4d8b80209152...
```

## JSON normalization

The jfpv1 JSON fingerprint function transforms the data internally into a normalized (canonical) format before hashing the output.

### Alternative specifications

Most existing JSON normalization/canonicalization specifications and related implementations operate on three key aspects: data structures, values and data ordering. While the ordering of key-value pairs (objects) is straightforward, issues usually arise from the ordering of arrays.

The JSON specifications, including the most recent [RFC 8259](https://tools.ietf.org/html/rfc8259), have always considered the order of array elements to be _meaningful_. As data gets serialized, transferred, deserialized and serialized again throughout various systems, maintaining the order of array elements becomes impractical if not impossible in many cases. As a consequence, this makes the creation and comparison of secure hashes of JSON data across multiple systems a complex process.

### JSON Fingerprint v1 (jfpv1)

The jfpv1 specification takes a more _value-oriented_ approach toward JSON normalization and secure hash creation: values and value-related metadata bear most significance when JSON data gets normalized into the jfpv1 format. The original JSON data gets transformed into a flattened list of small objects, which are then hashed and sorted, and ultimately hashed again as a whole.

In practice, the jfpv1 specification purposefully ignores the original order of data elements in an array. The jfpv1 specification focuses instead on verifying that the following aspects of JSON datasets being compared match:

 * All values in the compared datasets are identical
 * The values exist in identical paths (arrays, object key-value pairs)

In the case of arrays, each array gets a unique hash identifier based on the data elements it holds. This way, each flattened value "knows" to which array it belongs to. This identifier is called a _sibling hash_ because its derived from each value and its neighboring values.

## Running tests

The entire internal test suite of json-fingerprint is included in its distribution package. If you wish to run the internal test suite, install the package and run the following command:

`python -m json_fingerprint.tests.run`

If all tests ran successfully, this will produce an output similar to the following:

```
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.009s

OK
```

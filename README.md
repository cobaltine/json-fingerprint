# json-fingerprint

![](https://img.shields.io/github/license/cobaltine/json-fingerprint) ![](https://img.shields.io/pypi/pyversions/json-fingerprint) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Test%20runner/main) ![](https://img.shields.io/github/workflow/status/cobaltine/json-fingerprint/Release%20Python%20package/main?label=pypi%20release) [![](https://img.shields.io/pypi/v/json-fingerprint)](https://pypi.org/project/json-fingerprint/) ![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/cobaltine/json-fingerprint) [![Coverage Status](https://coveralls.io/repos/github/cobaltine/json-fingerprint/badge.svg?branch=main)](https://coveralls.io/github/cobaltine/json-fingerprint?branch=main)


Create consistent and comparable fingerprints (checksums/hashes) from unordered JSON data.

A json fingerprint consists of three parts: the version of the underlying algorithm, the hash function used and a hex digest of the hash function output. A complete example could look like this: `jfpv1$sha256$5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af`.

The first part indicates the algorithm version, `jfpv1`, which would translate to **j**son **f**inger**p**rint **v**ersion **1**. The second part, `sha256`, indicates that SHA256 is the hash function that was used. The last part, `5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af`, is a standard hex digest of the hash function output.


## Installation

To install the json-fingerprint package, run `pip install json-fingerprint`.


## Examples

The example below shows how to create and compare json fingerprints.

```python
import json
import json_fingerprint as jfp

obj_1_str = json.dumps([3, 2, 1, {'foo': 'bar'}])
obj_2_str = json.dumps([2, {'foo': 'bar'}, 1, 3])  # Same data in different order
fp_1 = jfp.json_fingerprint(input=obj_1_str, hash_function='sha256', version=1)
fp_2 = jfp.json_fingerprint(input=obj_2_str, hash_function='sha256', version=1)
print(f'Fingerprint 1: {fp_1}')
print(f'Fingerprint 2: {fp_2}')
```
This will output two identical fingerprints regardless of the different order of the json elements:

```
Fingerprint 1: jfpv1$sha256$287b67bce7ac4477011ba59ea55f168ba493508ffa6b61ef81594c9dab2c034f
Fingerprint 2: jfpv1$sha256$287b67bce7ac4477011ba59ea55f168ba493508ffa6b61ef81594c9dab2c034f
```

Since json objects with identical data content and structure will always produce identical fingerprints, the fingerprints can be used effectively for various purposes. These include finding duplicate json data from a larger dataset, json data cache validation/invalidation and data integrity checking.

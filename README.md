![](https://img.shields.io/github/license/cobaltine/json-fingerprint) ![](https://img.shields.io/pypi/pyversions/json-fingerprint) ![](https://img.shields.io/pypi/v/json-fingerprint) [![Coverage Status](https://coveralls.io/repos/github/cobaltine/json-fingerprint/badge.svg?branch=main)](https://coveralls.io/github/cobaltine/json-fingerprint?branch=main)

The **json-fingerprint** package provides easy checksum creation ("fingerprinting") from unordered JSON data.

## Installation and use

To install the package, run `pip install json-fingerprint`.

Below is a sample for creating simple fingerprints:

```
import json
import json_fingerprint as jfp

obj_1_str = json.dumps([3, 2, 1, {"foo": "bar"}])
obj_2_str = json.dumps([2, {"foo": "bar"}, 1, 3])
fp_1 = jfp.json_fingerprint(obj_1_str, hash_function='sha256', version=1)
fp_2 = jfp.json_fingerprint(obj_2_str, hash_function='sha256', version=1)
print(f'fp_1: {fp_1}')
print(f'fp_2: {fp_2}')
```
This will output two identical fingerprints regardless of the different ordering of the json elements:

```
fp_1: jfpv1$sha256$5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af
fp_2: jfpv1$sha256$5815eb0ce6f4e5ab0a771cce2a8c5432f64222f8fd84b4cc2d38e4621fae86af
```

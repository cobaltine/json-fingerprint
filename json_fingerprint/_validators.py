import re

from json_fingerprint import hash_functions

from .exceptions import (
    FingerprintPattern,
    FingerprintVersion,
    HashFunction,
    InputDataType,
)

SHA256_JFP_REGEX_PATTERN = re.compile("^jfpv1\\$sha256\\$[0-9a-f]{64}$")
SHA384_JFP_REGEX_PATTERN = re.compile("^jfpv1\\$sha384\\$[0-9a-f]{96}$")
SHA512_JFP_REGEX_PATTERN = re.compile("^jfpv1\\$sha512\\$[0-9a-f]{128}$")

JFPV1_HASH_FUNCTIONS = (
    hash_functions.SHA256,
    hash_functions.SHA384,
    hash_functions.SHA512,
)

JSON_FINGERPRINT_VERSIONS = (1,)


def _validate_hash_function(hash_function: str, version: int):
    if version == 1 and hash_function not in JFPV1_HASH_FUNCTIONS:
        err = f"Expected one of supported hash functions '{JFPV1_HASH_FUNCTIONS}', instead got '{hash_function}'"
        raise HashFunction(err)


def _validate_input_type(input: str):
    if type(input) is not str:
        err = f"Expected data type '{str}' (JSON in string format), instead got '{type(input)}'"
        raise InputDataType(err)


def _validate_version(version: int):
    if version not in JSON_FINGERPRINT_VERSIONS:
        err = f"Expected one of supported JSON fingerprint versions '{JSON_FINGERPRINT_VERSIONS}', instead got '{version}'"
        raise FingerprintVersion(err)


def _validate_fingerprint_format(fingerprint: str):
    is_valid = False

    if SHA256_JFP_REGEX_PATTERN.match(fingerprint) or SHA384_JFP_REGEX_PATTERN.match(fingerprint) or SHA512_JFP_REGEX_PATTERN.match(fingerprint):
        is_valid = True

    if not is_valid:
        err = "Expected JSON fingerprint in format '{fingerprint_version}${hash_function}${hex_digest}', " f"instead got: {fingerprint}"
        raise FingerprintPattern(err)

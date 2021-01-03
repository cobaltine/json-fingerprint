JFPV1_HASH_FUNCTIONS = (
    'sha256',
    'sha384',
    'sha512',
)

JSON_FINGERPRINT_VERSIONS = (
    1,
)


class FingerprintHashFunctionError(Exception):
    pass


class FingerprintInputDataTypeError(Exception):
    pass


class FingerprintVersionError(Exception):
    pass


def _validate_hash_function(hash_function: str, version: int):
    if hash_function not in JFPV1_HASH_FUNCTIONS:
        err = (f'Expected one of supported hash functions \'{JFPV1_HASH_FUNCTIONS}\', '
               f'instead got \'{hash_function}\'')
        raise FingerprintHashFunctionError(err)


def _validate_input_type(input: str):
    if type(input) is not str:
        err = f'Expected data type \'{type("")}\' (JSON in string format), instead got \'{type(input)}\''
        raise FingerprintInputDataTypeError(err)


def _validate_version(version: int):
    if version not in JSON_FINGERPRINT_VERSIONS:
        err = (f'Expected one of supported JSON fingerprint versions \'{JSON_FINGERPRINT_VERSIONS}\', '
               f'instead got \'{version}\'')
        raise FingerprintVersionError(err)

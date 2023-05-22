class FingerprintPattern(Exception):
    """The fingerprint pattern is not a valid JSON fingerprint pattern."""

    pass


class FingerprintVersion(Exception):
    """The fingerprint version is not a supported JSON fingerprint version."""

    pass


class HashFunction(Exception):
    """The hash function is not a supported JSON fingerprint hash function."""

    pass


class InputDataType(Exception):
    """The input data type is not string."""

    pass


class JSONLoad(Exception):
    """The input data is not valid JSON."""

    pass

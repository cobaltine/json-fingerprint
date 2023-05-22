import json
import unittest

from json_fingerprint import _validators, create, exceptions, hash_functions


class TestValidators(unittest.TestCase):
    def test_json_fingerprint_version(self):
        """Test JSON fingerprint FingerprintVersion exception.

        Verify that:
        - FingerprintVersion exception is properly raised with an unsupported version
        - FingerprintVersion exception is not raised with a supported version
        """
        with self.assertRaises(exceptions.FingerprintVersion):
            create(input=json.dumps({"foo": "bar"}), hash_function=hash_functions.SHA256, version=-1)

        _validators._validate_version(version=1)

        with self.assertRaises(exceptions.FingerprintVersion):
            _validators._validate_version(version=-1)

    def test_input_data_type(self):
        """Test jfpv1 input data type error.

        Verify that:
        - DataType exception is not raised with a valid string input
        - DataType exception is properly raised with a non-string input
        """
        with self.assertRaises(exceptions.InputDataType):
            create(input=123, hash_function=hash_functions.SHA256, version=1)

        try:
            _validators._validate_input_type(input="abc")
        except Exception as exc:
            err = "_validate_input_type() failed with a valid string"
            self.fail(f"{err}: {exc}")

        with self.assertRaises(exceptions.InputDataType):
            _validators._validate_input_type(input=123)

    def test_jfpv1_hash_function(self):
        """Test JSON fingerprint HashFunction exception.

        Verify that:
        - HashFunction exception is properly raised with an unsupported hash function selector
        - HashFunction exception is not raised with a supported hash function selector
        """
        with self.assertRaises(exceptions.HashFunction):
            create(input=json.dumps({"foo": "bar"}), hash_function="not123", version=1)

        try:
            _validators._validate_hash_function(hash_function=hash_functions.SHA256, version=1)
        except Exception as exc:
            err = "_validate_hash_function() failed with a valid hash function and version"
            self.fail(f"{err}: {exc}")

        with self.assertRaises(exceptions.HashFunction):
            _validators._validate_hash_function(hash_function="not123", version=1)

    def test_validate_fingerprint_pattern(self):
        """Test json fingerprint pattern validator.

        Verify that:
        - FingerprintPattern exception is not raised with a valid fingerprint
        - FingerprintPattern exception is raised with an invalid fingerprint
        """
        with self.assertRaises(exceptions.FingerprintPattern):
            _validators._validate_fingerprint_format(fingerprint="invalid fingerprint")

        input = json.dumps({"foo": "bar"})
        jfpv1_sha256 = create(input=input, hash_function=hash_functions.SHA256, version=1)
        jfpv1_sha384 = create(input=input, hash_function=hash_functions.SHA384, version=1)
        jfpv1_sha512 = create(input=input, hash_function=hash_functions.SHA512, version=1)

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha256)
        except Exception as exc:
            err = "_validate_fingerprint_format() failed with a valid json-sha256 fingerprint"
            self.fail(f"{err}: {exc}")

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha384)
        except Exception as exc:
            err = "_validate_fingerprint_format() failed with a valid json-sha384 fingerprint"
            self.fail(f"{err}: {exc}")

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha512)
        except Exception as exc:
            err = "_validate_fingerprint_format() failed with a valid json-sha512 fingerprint"
            self.fail(f"{err}: {exc}")

        fp = "jfpv1$exception_test"
        with self.assertRaises(exceptions.FingerprintPattern):
            _validators._validate_fingerprint_format(fingerprint=fp)


if __name__ == "__main__":
    unittest.main()

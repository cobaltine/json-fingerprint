import json
import unittest

from json_fingerprint import _exceptions, _validators, create


class TestValidators(unittest.TestCase):
    def test_json_fingerprint_version_error(self):
        """Test json fingerprint version selector error.

        Verify that:
        - FingerprintVersionError is properly raised with an unsupported version
        - FingerprintVersionError is not raised with a supported version"""
        with self.assertRaises(_exceptions.FingerprintVersionError):
            create(input=json.dumps({"foo": "bar"}), hash_function="sha256", version=-1)

        try:
            _validators._validate_version(version=1)
        except Exception:
            err = "_validate_version() failed with a valid version"
            self.fail(err)

        with self.assertRaises(_exceptions.FingerprintVersionError):
            _validators._validate_version(version=-1)

    def test_input_data_type_error(self):
        """Test jfpv1 input data type error.

        Verify that:
        - FingerprintInputDataTypeError is properly raised with a non-string input
        - FingerprintInputDataTypeError is not raised with a string input"""
        with self.assertRaises(_exceptions.FingerprintInputDataTypeError):
            create(input=123, hash_function="sha256", version=1)

        try:
            _validators._validate_input_type(input="abc")
        except Exception:
            err = "_validate_input_type() failed with a valid string"
            self.fail(err)

        with self.assertRaises(_exceptions.FingerprintInputDataTypeError):
            _validators._validate_input_type(input=123)

    def test_jfpv1_hash_function_error(self):
        """Test json fingerprint hash function selector error.

        Verify that:
        - FingerprintHashFunctionError is properly raised with an unsupported hash function selector
        - FingerprintHashFunctionError is not raised with a supported hash function selector"""
        with self.assertRaises(_exceptions.FingerprintHashFunctionError):
            create(input=json.dumps({"foo": "bar"}), hash_function="not123", version=1)

        try:
            _validators._validate_hash_function(hash_function="sha256", version=1)
        except Exception:
            err = "_validate_hash_function() failed with a valid hash function and version"
            self.fail(err)

        with self.assertRaises(_exceptions.FingerprintHashFunctionError):
            _validators._validate_hash_function(hash_function="not123", version=1)

    def test_validate_fingerprint_format(self):
        """Test json fingerprint format validator.

        Verify that:
        - FingerprintStringFormatError is properly raised with invalid fingerprint format
        - FingerprintStringFormatError is not raised with a valid fingerprint"""
        with self.assertRaises(_exceptions.FingerprintStringFormatError):
            _validators._validate_fingerprint_format(fingerprint="invalid fingerprint")

        input = json.dumps({"foo": "bar"})
        jfpv1_sha256 = create(input=input, hash_function="sha256", version=1)
        jfpv1_sha384 = create(input=input, hash_function="sha384", version=1)
        jfpv1_sha512 = create(input=input, hash_function="sha512", version=1)

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha256)
        except Exception:
            err = "_validate_fingerprint_format() failed with a valid json-sha256 fingerprint"
            self.fail(err)

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha384)
        except Exception:
            err = "_validate_fingerprint_format() failed with a valid json-sha384 fingerprint"
            self.fail(err)

        try:
            _validators._validate_fingerprint_format(fingerprint=jfpv1_sha512)
        except Exception:
            err = "_validate_fingerprint_format() failed with a valid json-sha512 fingerprint"
            self.fail(err)


if __name__ == "__main__":
    unittest.main()

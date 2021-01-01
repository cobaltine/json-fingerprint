import json
import unittest

from json_fingerprint import (
    _validators,
    json_fingerprint,
)


class TestValidators(unittest.TestCase):
    def test_jfpv1_json_fingerprint_version_error(self):
        """Test json fingerprint version selector error.

        Verify that:
        - FingerprintVersionError is properly raised with an unsupported version
        - FingerprintVersionError is not raised with a supported version"""
        with self.assertRaises(_validators.FingerprintVersionError):
            json_fingerprint(input=json.dumps({'foo': 'bar'}), hash_function='sha256', version=-1)

        try:
            _validators._validate_version(version=1)
        except Exception:
            err = '_validate_version() failed with a valid version'
            self.fail(err)

        with self.assertRaises(_validators.FingerprintVersionError):
            _validators._validate_version(version=-1)

    def test_jfpv1_input_data_type_error(self):
        """Test jfpv1 input data type error.

        Verify that:
        - FingerprintInputDataTypeError is properly raised with a non-string input
        - FingerprintInputDataTypeError is not raised with a string input"""
        with self.assertRaises(_validators.FingerprintInputDataTypeError):
            json_fingerprint(input=123, hash_function='sha256', version=1)

        try:
            _validators._validate_input_type(input='abc')
        except Exception:
            err = '_validate_input_type() failed with a valid string'
            self.fail(err)

        with self.assertRaises(_validators.FingerprintInputDataTypeError):
            _validators._validate_input_type(input=123)

    def test_jfpv1_hash_function_error(self):
        """Test json fingerprint hash function selector error.

        Verify that:
        - FingerprintHashFunctionError is properly raised with an unsupported hash function selector
        - FingerprintHashFunctionError is not raised with a supported hash function selector"""
        with self.assertRaises(_validators.FingerprintHashFunctionError):
            json_fingerprint(input=json.dumps(
                {'foo': 'bar'}), hash_function='not123', version=1)

        try:
            _validators._validate_hash_function(hash_function='sha256', version=1)
        except Exception:
            err = '_validate_hash_function() failed with a valid hash function and version'
            self.fail(err)

        with self.assertRaises(_validators.FingerprintHashFunctionError):
            _validators._validate_hash_function(hash_function='not123', version=1)


if __name__ == '__main__':
    unittest.main()

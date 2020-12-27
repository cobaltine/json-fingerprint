import json
import json_fingerprint as jfp
import unittest


class TestJsonFingerprint(unittest.TestCase):
    def test_jfpv1_json_fingerprint_version_error(self):
        """Test json fingerprint version selector error.

        Verify that:
        - FingerprintVersionError is properly raised with unsupported version"""
        with self.assertRaises(jfp.FingerprintVersionError):
            jfp.json_fingerprint(input=json.dumps(
                {'foo': 'bar'}), hash_function='sha256', version=-1)

    def test_jfpv1_input_data_type_error(self):
        """Test jfpv1 input data type error.

        Verify that:
        - FingerprintInputDataTypeError is properly raised with incorrect data type input (non-json)"""
        with self.assertRaises(jfp.FingerprintInputDataTypeError):
            jfp.json_fingerprint(input={'foo': 'bar'}, hash_function='sha256', version=1)

    def test_jfpv1_hash_function_error(self):
        """Test json fingerprint hash function selector error.

        Verify that:
        - FingerprintHashFunctionError is properly raised with unsupported hash function selector"""
        with self.assertRaises(jfp.FingerprintHashFunctionError):
            jfp.json_fingerprint(input=json.dumps(
                {'foo': 'bar'}), hash_function='not123', version=1)

    def test_jfpv1_json_load_error(self):
        """Test json fingerprint raw json string load error.

        Verify that:
        - FingerprintJSONLoadError is properly raised with malformed json input string"""
        with self.assertRaises(jfp.FingerprintJSONLoadError):
            jfp.json_fingerprint('{"foo": bar}', hash_function='sha256', version=1)


if __name__ == '__main__':
    unittest.main()

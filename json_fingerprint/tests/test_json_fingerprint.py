import json
import os
import unittest

from json_fingerprint import json_fingerprint
from json_fingerprint.json_fingerprint import FingerprintJSONLoadError

TESTS_DIR = os.path.dirname(__file__)
TESTDATA_DIR = os.path.join(TESTS_DIR, 'testdata')


class TestJsonFingerprint(unittest.TestCase):
    def test_jfpv1_json_load_error(self):
        """Test json fingerprint raw json string load error.

        Verify that:
        - FingerprintJSONLoadError is properly raised with malformed json input string"""
        with self.assertRaises(FingerprintJSONLoadError):
            json_fingerprint('{"foo": bar}', hash_function='sha256', version=1)

    def test_jfpv1_sha256_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = json_fingerprint(input='{"foo": "bar"}', hash_function='sha256', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha256\\$[0-9a-f]{64}$')

    def test_jfpv1_sha384_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = json_fingerprint(input='{"foo": "bar"}', hash_function='sha384', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha384\\$[0-9a-f]{96}$')

    def test_jfpv1_sha512_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = json_fingerprint(input='{"foo": "bar"}', hash_function='sha512', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha512\\$[0-9a-f]{128}$')

    def test_jfpv1_sha256_mixed_order(self):
        """Test jfpv1 sha256 mixed order fingerprint match.

        Verify that:
        - The fingerprints of test objects 1 and 2 match despite same data being ordered differently
        - The fingerprints also match against a known valid fingerprint"""
        with open(os.path.join(TESTDATA_DIR, 'jfpv1_test_obj_1.json'), 'r') as file:
            self.test_obj_1 = file.read()
            file.close()

        with open(os.path.join(TESTDATA_DIR, 'jfpv1_test_obj_2.json'), 'r') as file:
            self.test_obj_2 = file.read()
            file.close()
        fp_1 = json_fingerprint(self.test_obj_1, hash_function='sha256', version=1)
        fp_2 = json_fingerprint(self.test_obj_2, hash_function='sha256', version=1)
        self.assertEqual(fp_1, fp_2)
        self.assertEqual(fp_1, 'jfpv1$sha256$0b83bd27ab1227c6da76dc161f4fb4559f1876eb7fb4cc6257e675c8b4175cbd')

    def test_jfpv1_sha256_structural_distinction_1(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Identical value content in identical depths, but in different structures,
          don't produce identical outputs"""
        obj_in_1 = [
            1,
            [1, [2, 2]],
            [2, [2, 2]],
        ]
        fp_1 = json_fingerprint(input=json.dumps(obj_in_1), hash_function='sha256', version=1)

        obj_in_2 = [
            1,
            [1, 2, [2, 2, 2, 2]],
        ]
        fp_2 = json_fingerprint(input=json.dumps(obj_in_2), hash_function='sha256', version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_sha256_structural_distinction_2(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Values in identical paths/structures but different sibling values don't get matched"""
        obj_in_1 = [
            [1, ['x', 'x']],
            [2, ['y', 'y']],
        ]
        fp_1 = json_fingerprint(input=json.dumps(obj_in_1), hash_function='sha256', version=1)

        obj_in_2 = [
            [1, ['x', 'y']],
            [2, ['x', 'y']],
        ]
        fp_2 = json_fingerprint(input=json.dumps(obj_in_2), hash_function='sha256', version=1)

        self.assertNotEqual(fp_1, fp_2)


if __name__ == '__main__':
    unittest.main()
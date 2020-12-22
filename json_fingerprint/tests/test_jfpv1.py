import hashlib
import json
import json_fingerprint as jfp
import os
import unittest

TESTS_DIR = os.path.dirname(__file__)
TESTDATA_DIR = os.path.join(TESTS_DIR, 'testdata')


class TestJsonFingerprint(unittest.TestCase):
    def setUp(self):
        """Load test JSON objects.

        Test object 1 and test object 2 have identical values, but are ordered differently."""
        with open(os.path.join(TESTDATA_DIR, 'jfpv1_test_obj_1.json'), 'r') as file:
            self.test_obj_1 = file.read()
            file.close()

        with open(os.path.join(TESTDATA_DIR, 'jfpv1_test_obj_2.json'), 'r') as file:
            self.test_obj_2 = file.read()
            file.close()

    def test_jfpv1_sha256_mixed_order(self):
        """Test jfpv1 sha256 mixed order fingerprint match.

        Verify that:
        - The fingerprints of test objects 1 and 2 match despite same data being ordered differently sdaflk jsadlfkjsad fölksadj ödsf
        - The fingerprints also match against a known valid fingerprint"""
        fp_1 = jfp.json_fingerprint(self.test_obj_1, hash_function='sha256', version=1)
        fp_2 = jfp.json_fingerprint(self.test_obj_2, hash_function='sha256', version=1)
        self.assertEqual(fp_1, fp_2)
        self.assertEqual(fp_1,
                         'jfpv1$sha256$374833ebcdfda6ae4bf720ef9b6f9ba3dbd8cb82aca3b15ec9247db1f5f8f0b7')

    def test_jfpv1_sha256_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = jfp.json_fingerprint('{"foo": "bar"}', hash_function='sha256', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha256\\$[0-9a-f]{64}$')

    def test_jfpv1_json_fingerprint_version_error(self):
        """Test JSON fingerprint version selector error.

        Verify that:
        - FingerprintVersionError is properly raised with unsupported version"""
        with self.assertRaises(jfp.FingerprintVersionError):
            jfp.json_fingerprint(input=self.test_obj_1, hash_function='sha256', version=-1)

    def test_jfpv1_input_data_type_error(self):
        """Test jfpv1 input data type error.

        Verify that:
        - FingerprintInputDataTypeError is properly raised with incorrect data type input"""
        with self.assertRaises(jfp.FingerprintInputDataTypeError):
            jfp.json_fingerprint(input={'foo': 'bar'}, hash_function='sha256', version=1)

    def test_jfpv1_hash_function_error(self):
        """Test JSON fingerprint hash function selector error.

        Verify that:
        - FingerprintHashFunctionError is properly raised with unsupported hash function selector"""
        with self.assertRaises(jfp.FingerprintHashFunctionError):
            jfp.json_fingerprint(input=self.test_obj_1, hash_function='not123', version=1)

    def test_jfpv1_json_load_error(self):
        """Test JSON fingerprint raw JSON string load error.

        Verify that:
        - FingerprintJSONLoadError is properly raised with malformed JSON input string"""
        with self.assertRaises(jfp.FingerprintJSONLoadError):
            jfp.json_fingerprint('{"foo": bar}', hash_function='sha256', version=1)

    def test_jfpv1_flattened_json_list_format(self):
        """Test jfpv1 JSON flattener.

        Verify that:
        - jfpv1 JSON flattener produces objects of expected output format"""
        obj_in = [
            False,
            True,
            1,
            "a",
            {"foo": "bar"},
            [1, [2, 3]],
        ]

        obj_out = []
        jfp._flatten_json(data=obj_in, out=obj_out)

        expected_obj_out = [
            {'path': '[6]', 'value': False},
            {'path': '[6]', 'value': True},
            {'path': '[6]', 'value': 1},
            {'path': '[6]', 'value': 'a'},
            {'path': '[6]|{foo}', 'value': 'bar'},
            {'path': '[6]|[2]', 'value': 1},
            {'path': '[6]|[2]|[2]', 'value': 2},
            {'path': '[6]|[2]|[2]', 'value': 3},
        ]

        self.assertEqual(len(obj_out), len(expected_obj_out))

        for i in range(len(expected_obj_out)):
            self.assertEqual(obj_out[i], expected_obj_out[i])

    def test_jfpv1_flattened_json_depth_handling(self):
        """Test jfpv1 JSON flattener depth handling.

        Verify that:
        - Identical value content in different structures (depths) don't prodcue same outputs"""
        obj_in_1 = [
            1,
            [1, [2, 2]],
            [2, [2, 2]],
        ]
        obj_out_1 = []
        jfp._flatten_json(data=obj_in_1, out=obj_out_1)

        obj_in_2 = [
            1,
            [1, 2, [2, 2, 2, 2]],
        ]
        obj_out_2 = []
        jfp._flatten_json(data=obj_in_2, out=obj_out_2)

        self.assertNotEqual(obj_out_1, obj_out_2)

    def test_jfpv1_create_hash_list(self):
        """Test jfpv1 hash list, used for condensing unique identifiers into an easily sortable list.

        Verify that:
        - The hash list produces valid SHA256 hashes
        - Sorts the hashes properly"""

        input_data = [
            {'path': '[6]', 'value': False},
            {'path': '[6]|{foo}', 'value': 'bar'},
            {'path': '[6]|[2]|[2]', 'value': 3},
        ]

        # Output prior to sorting:
        # ['b95942007889a3e01bd12cbb81f79a5c1ddc5483a597434406ce71a947d7ab12',
        # 'eecd2594dff9f6fbd9d4453ec8c1814b86436d3c7aa2682139872cc7cc78120c',
        # 'cc95192597ed8a7486387c5ca3dfeb3ef8e57eee4dd3ec3be45f203fa2029137']
        output_data_hashes = jfp._create_hash_list(data=input_data)

        input_data_hashes = []
        for i in range(len(input_data)):
            stringified = json.dumps(input_data[i], sort_keys=True)
            m = hashlib.sha256()
            m.update(stringified.encode('utf-8'))
            input_data_hashes.append(m.hexdigest())
        input_data_hashes.sort()

        for i in range(len(output_data_hashes)):
            self.assertEqual(input_data_hashes[i], output_data_hashes[i])


if __name__ == '__main__':
    unittest.main()

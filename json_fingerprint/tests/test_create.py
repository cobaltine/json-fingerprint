import json
import os
import unittest

from json_fingerprint import create, hash_functions
from json_fingerprint.exceptions import JSONLoad

TESTS_DIR = os.path.dirname(__file__)
TESTDATA_DIR = os.path.join(TESTS_DIR, "testdata")


class TestCreate(unittest.TestCase):
    def test_jfpv1_json_load_error(self):
        """Test json fingerprint raw json string load error.

        Verify that:
        - FingerprintJSONLoadError is properly raised with malformed json input string
        """
        with self.assertRaises(JSONLoad):
            create('{"foo": bar}', hash_function=hash_functions.SHA256, version=1)

    def test_jfpv1_sha256_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted
        """
        fp = create(input='{"foo": "bar"}', hash_function=hash_functions.SHA256, version=1)
        self.assertRegex(fp, "^jfpv1\\$sha256\\$[0-9a-f]{64}$")

    def test_jfpv1_sha384_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted
        """
        fp = create(input='{"foo": "bar"}', hash_function=hash_functions.SHA384, version=1)
        self.assertRegex(fp, "^jfpv1\\$sha384\\$[0-9a-f]{96}$")

    def test_jfpv1_sha512_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted
        """
        fp = create(input='{"foo": "bar"}', hash_function=hash_functions.SHA512, version=1)
        self.assertRegex(fp, "^jfpv1\\$sha512\\$[0-9a-f]{128}$")

    def test_jfpv1_sha256_mixed_order(self):
        """Test jfpv1 sha256 mixed order fingerprint match.

        Verify that:
        - The fingerprints of test objects 1 and 2 match despite same data being ordered differently
        - The fingerprints also match against a known valid fingerprint
        """
        with open(os.path.join(TESTDATA_DIR, "jfpv1_test_obj_1.json"), "r") as file:
            self.test_obj_1 = file.read()
            file.close()

        with open(os.path.join(TESTDATA_DIR, "jfpv1_test_obj_2.json"), "r") as file:
            self.test_obj_2 = file.read()
            file.close()
        fp_1 = create(self.test_obj_1, hash_function=hash_functions.SHA256, version=1)
        fp_2 = create(self.test_obj_2, hash_function=hash_functions.SHA256, version=1)
        self.assertEqual(fp_1, fp_2)
        self.assertEqual(fp_1, "jfpv1$sha256$b182c755347a6884fd11f1194cbe0961f548e5ac62be78a56c48c3c05eb56650")

    def test_jfpv1_sha256_structural_distinction_1(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Identical values at identical depths, but held in different data structures,
          don't produce identical outputs
        """
        obj_in_1 = [
            1,
            [1, [2, 2]],
            [2, [2, 2]],
        ]
        fp_1 = create(input=json.dumps(obj_in_1), hash_function=hash_functions.SHA256, version=1)

        obj_in_2 = [
            1,
            [1, 2, [2, 2, 2, 2]],
        ]
        fp_2 = create(input=json.dumps(obj_in_2), hash_function=hash_functions.SHA256, version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_sha256_structural_distinction_2(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Values in identical data structure paths, but different sibling values, don't get matched
        """
        obj_in_1 = [
            [1, ["x", "x"]],
            [2, ["y", "y"]],
        ]
        fp_1 = create(input=json.dumps(obj_in_1), hash_function=hash_functions.SHA256, version=1)

        obj_in_2 = [
            [1, ["x", "y"]],
            [2, ["x", "y"]],
        ]
        fp_2 = create(input=json.dumps(obj_in_2), hash_function=hash_functions.SHA256, version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_empty_list_as_value(self):
        """Test jfpv1 json flattener's ability to handle empty lists as values.

        Versions up to 0.12.2 did not acknowledge empty lists as values.
        Related issue: https://github.com/cobaltine/json-fingerprint/issues/33

        Verify that:
        - Empty lists (and, as such, underlying data structure paths) are not ignored by the json flattener
        """
        obj_in_1 = {"field1": "yes"}
        fp_1 = create(input=json.dumps(obj_in_1), hash_function=hash_functions.SHA256, version=1)

        obj_in_2 = {"field1": "yes", "field2": []}
        fp_2 = create(input=json.dumps(obj_in_2), hash_function=hash_functions.SHA256, version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_empty_dict_as_value(self):
        """Test jfpv1 json flattener's ability to handle empty dicts as values.

        Versions up to 0.12.2 did not acknowledge empty dicts as values.
        Related issue: https://github.com/cobaltine/json-fingerprint/issues/33

        Verify that:
        - Empty dicts (and, as such, underlying data structure paths) are not ignored by the json flattener"""

        obj_in_1 = {"field1": "yes"}
        fp_1 = create(input=json.dumps(obj_in_1), hash_function=hash_functions.SHA256, version=1)

        obj_in_2 = {"field1": "yes", "field2": {}}
        fp_2 = create(input=json.dumps(obj_in_2), hash_function=hash_functions.SHA256, version=1)

        self.assertNotEqual(fp_1, fp_2)


if __name__ == "__main__":
    unittest.main()

import json_fingerprint as jfp
import os
import unittest

TESTS_DIR = os.path.dirname(__file__)
TESTDATA_DIR = os.path.join(TESTS_DIR, 'testdata')


class TestJsonFingerprint(unittest.TestCase):
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
        fp_1 = jfp.json_fingerprint(self.test_obj_1, hash_function='sha256', version=1)
        fp_2 = jfp.json_fingerprint(self.test_obj_2, hash_function='sha256', version=1)
        self.assertEqual(fp_1, fp_2)
        self.assertEqual(fp_1, 'jfpv1$sha256$0b83bd27ab1227c6da76dc161f4fb4559f1876eb7fb4cc6257e675c8b4175cbd')


if __name__ == '__main__':
    unittest.main()

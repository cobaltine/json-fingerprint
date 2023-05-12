import json
import unittest

from json_fingerprint import _exceptions, _find_matches, create


class TestFindMatches(unittest.TestCase):
    def setUp(self):
        self.test_input = json.dumps({"foo": "bar"})
        self.jfpv1_sha256 = create(input=self.test_input, hash_function="sha256", version=1)
        self.jfpv1_sha384 = create(input=self.test_input, hash_function="sha384", version=1)
        self.jfpv1_sha512 = create(input=self.test_input, hash_function="sha512", version=1)

    def test_get_target_hashes(self):
        """Test target hash list creation.

        Verify that:
        - The returned element list contains only unique entries"""
        # Fingerprint list with duplicate entries
        fingerprints = [
            self.jfpv1_sha256,
            self.jfpv1_sha256,
            self.jfpv1_sha384,
            self.jfpv1_sha512,
            self.jfpv1_sha512,
        ]

        target_hashes = _find_matches._get_target_hashes(fingerprints=fingerprints)
        self.assertEqual(len(target_hashes), 3)

        expected_elements = [
            {"version": 1, "hash_function": "sha256"},
            {"version": 1, "hash_function": "sha384"},
            {"version": 1, "hash_function": "sha512"},
        ]
        self.assertEqual(expected_elements, target_hashes)

    def test_create_input_fingerprints(self):
        """Test list matching's fingerprint creation function.

        Verify that:
        - Fingerprints are correctly parsed from the given target hash elements"""
        target_hashes = [
            {"version": 1, "hash_function": "sha256"},
            {"version": 1, "hash_function": "sha384"},
            {"version": 1, "hash_function": "sha512"},
        ]

        input_fingerprints = _find_matches._create_input_fingerprints(input=self.test_input, target_hashes=target_hashes)
        self.assertEqual(len(input_fingerprints), 3)
        self.assertIn(self.jfpv1_sha256, input_fingerprints)
        self.assertIn(self.jfpv1_sha384, input_fingerprints)
        self.assertIn(self.jfpv1_sha512, input_fingerprints)

    def test_jfpv1_find_matches(self):
        """Test json fingerprint list matcher.

        Verify that:
        - Fingerprints of all jfpv1 SHA-2 variants are properly matched in a fingerprint list
        - Deduplication works for duplicate entries in fingerprint list
        - Exceptions are properly raised with invalid fingerprints and input types"""
        input = json.dumps({"bar": "foo"})
        chaff_jfpv1_sha256 = create(input=input, hash_function="sha256", version=1)

        # Fingerprint list with duplicate entries
        fingerprints = [
            # Expected matches (5)
            self.jfpv1_sha256,
            self.jfpv1_sha256,
            self.jfpv1_sha384,
            self.jfpv1_sha512,
            self.jfpv1_sha512,
            # Chaff
            chaff_jfpv1_sha256,
        ]

        matches = _find_matches.find_matches(input=self.test_input, fingerprints=fingerprints)
        self.assertEqual(len(matches), 5)

        deduplicated_matches = _find_matches.find_matches(input=self.test_input, fingerprints=fingerprints, deduplicate=True)
        self.assertEqual(len(deduplicated_matches), 3)

        with self.assertRaises(_exceptions.FingerprintJSONLoadError):
            _find_matches.find_matches(input='{"invalid": json string}', fingerprints=[self.jfpv1_sha256])
        with self.assertRaises(_exceptions.FingerprintStringFormatError):
            _find_matches.find_matches(input=input, fingerprints=["invalid fingerprint string"])


if __name__ == "__main__":
    unittest.main()

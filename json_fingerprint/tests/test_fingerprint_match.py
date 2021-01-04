import json
import unittest

from json_fingerprint import (
    _exceptions,
    fingerprint_match,
    json_fingerprint,
)


class TestFingerprintMatch(unittest.TestCase):
    def test_jfpv1_fingerprint_match(self):
        """Test json fingerprint matcher.

        Verify that:
        - Fingerprints of all jfpv1 SHA-2 variants are properly matched
        - Exception is properly raised with invalid fingerprints and input types"""
        input = json.dumps({'foo': 'bar'})
        jfpv1_sha256 = json_fingerprint(input=input, hash_function='sha256', version=1)
        jfpv1_sha384 = json_fingerprint(input=input, hash_function='sha384', version=1)
        jfpv1_sha512 = json_fingerprint(input=input, hash_function='sha512', version=1)

        match_sha256 = fingerprint_match(input=input, target_fingerprint=jfpv1_sha256)
        self.assertEqual(match_sha256, True)
        match_sha384 = fingerprint_match(input=input, target_fingerprint=jfpv1_sha384)
        self.assertEqual(match_sha384, True)
        match_sha512 = fingerprint_match(input=input, target_fingerprint=jfpv1_sha512)
        self.assertEqual(match_sha512, True)

        no_match = fingerprint_match(input=json.dumps('{"bar": "foo"}'), target_fingerprint=jfpv1_sha256)
        self.assertEqual(no_match, False)

        with self.assertRaises(_exceptions.FingerprintJSONLoadError):
            fingerprint_match(input='{"invalid": json string}', target_fingerprint=jfpv1_sha256)
        with self.assertRaises(_exceptions.FingerprintStringFormatError):
            fingerprint_match(input=input, target_fingerprint='invalid fingerprint string')


if __name__ == '__main__':
    unittest.main()
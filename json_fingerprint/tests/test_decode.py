import json
import unittest

from json_fingerprint import _exceptions, create, decode


class TestDecode(unittest.TestCase):
    def test_jfpv1_decode(self):
        """Test json fingerprint decoder.

        Verify that:
        - Fingerprints of all jfpv1 SHA-2 variants are properly decoded
        - Exception is properly raised with invalid fingerprint input
        """
        input = json.dumps({"foo": "bar"})
        jfpv1_sha256 = create(input=input, hash_function="sha256", version=1)
        jfpv1_sha384 = create(input=input, hash_function="sha384", version=1)
        jfpv1_sha512 = create(input=input, hash_function="sha512", version=1)

        version, hash_function, hash = decode(fingerprint=jfpv1_sha256)
        self.assertEqual(version, 1)
        self.assertEqual(hash_function, "sha256")
        self.assertEqual(hash, jfpv1_sha256.split("$")[-1])

        version, hash_function, hash = decode(fingerprint=jfpv1_sha384)
        self.assertEqual(version, 1)
        self.assertEqual(hash_function, "sha384")
        self.assertEqual(hash, jfpv1_sha384.split("$")[-1])

        version, hash_function, hash = decode(fingerprint=jfpv1_sha512)
        self.assertEqual(version, 1)
        self.assertEqual(hash_function, "sha512")
        self.assertEqual(hash, jfpv1_sha512.split("$")[-1])

        with self.assertRaises(_exceptions.FingerprintStringFormatError):
            decode(fingerprint="invalid fingerprint")


if __name__ == "__main__":
    unittest.main()

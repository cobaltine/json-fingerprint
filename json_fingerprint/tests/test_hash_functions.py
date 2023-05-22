import json
import unittest

from json_fingerprint import _validators, create, exceptions, hash_functions


class TestHashFunctions(unittest.TestCase):
    def test_hash_function_module_options(self):
        """Test the 'hash_functions' module's SHA-2 options.

        Verify that:
        - Each supported hash function string is available ("sha256", "sha384", and "sha512")
        - The options are all-lowercase (exact match)
        """
        self.assertEqual(hash_functions.SHA256, "sha256")
        self.assertEqual(hash_functions.SHA384, "sha384")
        self.assertEqual(hash_functions.SHA512, "sha512")


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import unittest

from json_fingerprint import _jfpv1


class TestJfpv1(unittest.TestCase):
    def test_create_json_hash(self):
        """Test jfpv1 json sha256 hash creation

        Verify that:
        - Key-value pairs are sorted properly and the resulting SHA256 matches the expected hash
        """
        data = {"value": "bar", "path": "{foo}"}
        stringified = json.dumps(
            data,
            allow_nan=False,
            ensure_ascii=False,
            indent=None,
            separators=(",", ":"),
            skipkeys=False,
            sort_keys=True,
        )
        m = hashlib.sha256()
        m.update(stringified.encode("utf-8"))
        expected_hex_digest = m.hexdigest()
        hex_digest = _jfpv1._create_json_hash(data=data, hash_function="sha256")
        self.assertEqual(hex_digest, expected_hex_digest)

    def test_jfpv1_create_sorted_hash_list(self):
        """Test jfpv1 hash list used for condensing unique identifiers into an easily sortable list

        Verify that:
        - The hash list produces valid SHA256 hashes from json-formatted data
        - Sorts the hashes properly
        """
        input_data = [
            # SHA256 (json-formatted): ac8d8342bbb2362d13f0a559a3621bb407011368895164b628a54f7fc33fc43c
            "a",
            # SHA256 (json-formatted): c100f95c1913f9c72fc1f4ef0847e1e723ffe0bde0b36e5f36c13f81fe8c26ed
            "b",
            # SHA256 (json-formatted): 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d
            "c",
        ]

        output_data_hashes = _jfpv1._create_sorted_hash_list(data=input_data, hash_function="sha256")
        input_data_hashes = []
        for datum in input_data:
            m = hashlib.sha256()
            json_formatted_input = json.dumps(datum)
            m.update(json_formatted_input.encode("utf-8"))
            input_data_hashes.append(m.hexdigest())
        input_data_hashes.sort()

        self.assertEqual(input_data_hashes, output_data_hashes)

    def test_jfpv1_build_path(self):
        """Test jfpv1 raw path formatting

        Verify that:
        - Path list and dict element encapsulation work as intended
        - Combination paths are separated properly (pipe character)
        - List and dict indicators, and path separator, display correctly even if same
          characters ([]{}|) are used in dict field names
        """
        root = ""
        dict_key = "{foo}"  # Dict with a field named 'foo'
        list_key = "[5]"  # List with 5 elements in it

        dict_root_path = _jfpv1._build_path(key=dict_key, base_path=root)
        self.assertEqual(dict_root_path, "{foo}")

        list_root_path = _jfpv1._build_path(key=list_key, base_path=root)
        self.assertEqual(list_root_path, "[5]")

        combination_path = _jfpv1._build_path(key=dict_key, base_path=list_key)
        self.assertEqual(combination_path, "[5]|{foo}")

        obj_out_raw = _jfpv1._flatten_json(data=[1, {"[1]|{foo}": "bar"}, 2], hash_function="sha256")
        self.assertEqual(obj_out_raw[0]["path"], "[3]")
        self.assertEqual(obj_out_raw[1]["path"], "[3]|{[1]|{foo}}")
        self.assertEqual(obj_out_raw[2]["path"], "[3]")

    def test_build_element(self):
        without_siblings_val = _jfpv1._build_element(path="{foo}", siblings=[], value="bar")
        self.assertEqual(without_siblings_val, {"path": "{foo}", "value": "bar"})
        with_siblings_val = _jfpv1._build_element(path="[2]", siblings="abc", value="foo")
        self.assertEqual(with_siblings_val, {"path": "[2]", "siblings": "abc", "value": "foo"})

    def test_jfpv1_flattened_json_sha256_fingerprint(self):
        """Test jfpv1 json flattener and fingerprint creation

        Verify that:
        - jfpv1 json flattener produces expected raw output format (non-hashed siblings in debug mode)
        - jfpv1 json flattener produces expected standard output format (hashed siblings)
        - jfpv1 json flattener output will produce valid jfpv1 fingerprints
        """
        obj_in = [
            1,
            [2, 3],
        ]
        obj_out_raw = _jfpv1._flatten_json(data=obj_in, hash_function="sha256", debug=True)
        expected_obj_out_raw = [
            {
                "path": "[2]",
                "siblings": [
                    {"path": "[2]", "value": 1},
                    {"path": "[2]|[2]", "siblings": [{"path": "[2]|[2]", "value": 2}, {"path": "[2]|[2]", "value": 3}], "value": 2},
                    {"path": "[2]|[2]", "siblings": [{"path": "[2]|[2]", "value": 2}, {"path": "[2]|[2]", "value": 3}], "value": 3},
                ],
                "value": 1,
            },
            {"path": "[2]|[2]", "siblings": [{"path": "[2]|[2]", "value": 2}, {"path": "[2]|[2]", "value": 3}], "value": 2},
            {"path": "[2]|[2]", "siblings": [{"path": "[2]|[2]", "value": 2}, {"path": "[2]|[2]", "value": 3}], "value": 3},
        ]
        self.assertEqual(obj_out_raw, expected_obj_out_raw)

        obj_out = _jfpv1._flatten_json(data=obj_in, hash_function="sha256")
        inner_list_siblings_hash_list = _jfpv1._create_sorted_hash_list(
            [{"path": "[2]|[2]", "value": 2}, {"path": "[2]|[2]", "value": 3}], hash_function="sha256"
        )
        siblings_1 = _jfpv1._create_sorted_hash_list(
            [
                {"path": "[2]", "value": 1},
                {"path": "[2]|[2]", "siblings": _jfpv1._create_json_hash(data=inner_list_siblings_hash_list, hash_function="sha256"), "value": 2},
                {"path": "[2]|[2]", "siblings": _jfpv1._create_json_hash(data=inner_list_siblings_hash_list, hash_function="sha256"), "value": 3},
            ],
            hash_function="sha256",
        )
        expected_out_hash_lists = [
            {"path": "[2]", "siblings": _jfpv1._create_json_hash(data=siblings_1, hash_function="sha256"), "value": 1},
            {"path": "[2]|[2]", "siblings": _jfpv1._create_json_hash(data=inner_list_siblings_hash_list, hash_function="sha256"), "value": 2},
            {"path": "[2]|[2]", "siblings": _jfpv1._create_json_hash(data=inner_list_siblings_hash_list, hash_function="sha256"), "value": 3},
        ]
        self.assertEqual(obj_out, expected_out_hash_lists)

        sorted_hash_list = _jfpv1._create_sorted_hash_list(data=obj_out, hash_function="sha256")
        hex_digest = _jfpv1._create_json_hash(data=sorted_hash_list, hash_function="sha256")
        jfpv1_out_1 = f"jfpv1$sha256${hex_digest}"
        jfpv1_out_2 = _jfpv1._create_jfpv1_fingerprint(data=obj_in, hash_function="sha256", version=1)
        self.assertEqual(jfpv1_out_1, jfpv1_out_2)

    def test_jfpv1_json_flattener_primitive_integer_handling(self):
        """Test jfpv1 primitive integer handling

        Verify that:
        - Integers are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint
        """
        int_val = 123
        int_out_raw = _jfpv1._flatten_json(data=int_val, hash_function="sha256")
        expected_int_out_raw = [{"path": "", "value": int_val}]
        self.assertEqual(int_out_raw, expected_int_out_raw)

    def test_jfpv1_json_flattener_primitive_float_handling(self):
        """Test jfpv1 primitive float handling

        Verify that:
        - Floats are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint
        """
        float_val = 123.321
        float_out_raw = _jfpv1._flatten_json(data=float_val, hash_function="sha256")
        expected_float_out_raw = [{"path": "", "value": float_val}]
        self.assertEqual(float_out_raw, expected_float_out_raw)

    def test_jfpv1_json_flattener_primitive_string_handling(self):
        """Test jfpv1 primitive string handling

        Verify that:
        - Strings are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint
        """
        string_val = "alpha 123"
        string_out_raw = _jfpv1._flatten_json(data=string_val, hash_function="sha256")
        expected_string_out_raw = [{"path": "", "value": string_val}]
        self.assertEqual(string_out_raw, expected_string_out_raw)

    def test_jfpv1_json_flattener_primitive_boolean_handling(self):
        """Test jfpv1 primitive boolean handling

        Verify that:
        - Booleans are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint
        """
        bool_val = True
        bool_out_raw = _jfpv1._flatten_json(data=bool_val, hash_function="sha256")
        expected_bool_out_raw = [{"path": "", "value": bool_val}]
        self.assertEqual(bool_out_raw, expected_bool_out_raw)

    def test_jfpv1_json_flattener_primitive_none_handling(self):
        """Test jfpv1 primitive boolean handling

        Verify that:
        - Booleans are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint
        """
        none_val = None
        none_out_raw = _jfpv1._flatten_json(data=none_val, hash_function="sha256")
        expected_bool_out_raw = [{"path": "", "value": none_val}]
        self.assertEqual(none_out_raw, expected_bool_out_raw)

    def test_jfpv1_json_flattener_empty_list_handling(self):
        """Test jfpv1 json flattener's ability to handle empty lists as values

        Versions up to v0.12.2 did not acknowledge empty lists as values.
        Related issue: https://github.com/cobaltine/json-fingerprint/issues/33

        Verify that:
        - Empty lists are considered to be values"""

        empty_list_val = []
        empty_list_out_raw = _jfpv1._flatten_json(data=empty_list_val, hash_function="sha256")
        expected_emtpy_list_out_raw = [{"path": "", "value": empty_list_val}]
        self.assertEqual(empty_list_out_raw, expected_emtpy_list_out_raw)

    def test_jfpv1_json_flattener_empty_dict_handling(self):
        """Test jfpv1 json flattener's ability to handle empty dicts as values

        Versions up to v0.12.2 did not acknowledge empty dicts as values.
        Related issue: https://github.com/cobaltine/json-fingerprint/issues/33

        Verify that:
        - Empty dicts are considered to be values"""

        empty_dict_val = {}
        empty_dict_out_raw = _jfpv1._flatten_json(data=empty_dict_val, hash_function="sha256")
        expected_empty_dict_out_raw = [{"path": "", "value": empty_dict_val}]
        self.assertEqual(empty_dict_out_raw, expected_empty_dict_out_raw)


if __name__ == "__main__":
    unittest.main()

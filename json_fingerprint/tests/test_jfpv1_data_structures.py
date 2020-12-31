import hashlib
import json
import json_fingerprint as jfp
import unittest


class TestJsonFingerprint(unittest.TestCase):
    def test_jfpv1_sha256_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = jfp.json_fingerprint(input='{"foo": "bar"}', hash_function='sha256', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha256\\$[0-9a-f]{64}$')

    def test_jfpv1_create_sorted_sha256_hash_list(self):
        """Test jfpv1 hash list, used for condensing unique identifiers into an easily sortable list.

        Verify that:
        - The hash list produces valid SHA256 hashes from json-formatted data
        - Sorts the hashes properly"""
        input_data = [
            # SHA256 (json-formatted): ac8d8342bbb2362d13f0a559a3621bb407011368895164b628a54f7fc33fc43c
            'a',
            # SHA256 (json-formatted): c100f95c1913f9c72fc1f4ef0847e1e723ffe0bde0b36e5f36c13f81fe8c26ed
            'b',
            # SHA256 (json-formatted): 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d
            'c',
        ]

        output_data_hashes = jfp._create_sorted_sha256_hash_list(data=input_data)
        input_data_hashes = []
        for datum in input_data:
            m = hashlib.sha256()
            json_formatted_input = json.dumps(datum)
            m.update(json_formatted_input.encode('utf-8'))
            input_data_hashes.append(m.hexdigest())
        input_data_hashes.sort()

        self.assertEqual(input_data_hashes, output_data_hashes)

    def test_jfpv1_build_path(self):
        """Test jfpv1 raw path formatting.

        Verify that:
        - Path list and dict element encapsulation work as intended
        - Combination paths are separated properly (pipe character)
        - List and dict indicators, and path separator, display correctly even if same
          characters ([]{}|) are used in dict field names"""
        root = ''
        dict_key = '{foo}'  # Dict with a field named 'foo'
        list_key = '[5]'  # List with 5 elements in it

        dict_root_path = jfp._build_path(key=dict_key, base_path=root)
        self.assertEqual(dict_root_path, '{foo}')

        list_root_path = jfp._build_path(key=list_key, base_path=root)
        self.assertEqual(list_root_path, '[5]')

        combination_path = jfp._build_path(key=dict_key, base_path=list_key)
        self.assertEqual(combination_path, '[5]|{foo}')

        obj_out_raw = jfp._flatten_json(data=[1, {'[1]|{foo}': 'bar'}, 2], debug=False)
        self.assertEqual(obj_out_raw[0]['path'], '[3]')
        self.assertEqual(obj_out_raw[1]['path'], '[3]|{[1]|{foo}}')
        self.assertEqual(obj_out_raw[2]['path'], '[3]')

    def test_jfpv1_sha256_primitive_integer_handling(self):
        """Test jfpv1 primitive integer handling.

        Verify that:
        - Integers are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        int_val = 123
        int_out_raw = jfp._flatten_json(data=int_val)
        expected_int_out_raw = [{'path': '', 'value': int_val}]
        self.assertEqual(int_out_raw, expected_int_out_raw)
        int_fp = jfp.json_fingerprint(input=json.dumps(int_val), hash_function='sha256', version=1)
        self.assertEqual(int_fp, 'jfpv1$sha256$a16c18417324d5bd1c995ae04e2caebe82bad8fb0873552b04ec877d0663c7f9')

    def test_jfpv1_sha256_primitive_float_handling(self):
        """Test jfpv1 primitive float handling.

        Verify that:
        - Floats are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        float_val = 123.321
        float_out_raw = jfp._flatten_json(data=float_val)
        expected_float_out_raw = [{'path': '', 'value': float_val}]
        self.assertEqual(float_out_raw, expected_float_out_raw)
        float_fp = jfp.json_fingerprint(input=json.dumps(float_val), hash_function='sha256', version=1)
        self.assertEqual(float_fp, 'jfpv1$sha256$d442ad64640e19a39d23017d18369de342d19c727ee2b4998e51a768fe0d5f71')

    def test_jfpv1_sha256_primitive_string_handling(self):
        """Test jfpv1 primitive string handling.

        Verify that:
        - Strings are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        string_val = 'alpha 123'
        string_out_raw = jfp._flatten_json(data=string_val)
        expected_string_out_raw = [{'path': '', 'value': string_val}]
        self.assertEqual(string_out_raw, expected_string_out_raw)
        string_fp = jfp.json_fingerprint(input=json.dumps(string_val), hash_function='sha256', version=1)
        self.assertEqual(string_fp, 'jfpv1$sha256$a4a03ce832454f6e5a93a7815447d35f10f90175a12c9b8b4bece0ec39fa610f')

    def test_jfpv1_sha256_primitive_boolean_handling(self):
        """Test jfpv1 primitive boolean handling.

        Verify that:
        - Booleans are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        bool_val = True
        bool_out_raw = jfp._flatten_json(data=bool_val)
        expected_bool_out_raw = [{'path': '', 'value': bool_val}]
        self.assertEqual(bool_out_raw, expected_bool_out_raw)
        bool_fp = jfp.json_fingerprint(input=json.dumps(bool_val), hash_function='sha256', version=1)
        self.assertEqual(bool_fp, 'jfpv1$sha256$30331f53262ff580f83f194998035131138100e8e6ee3e439c1cab3c77b7212e')

    def test_jfpv1_sha256_primitive_none_handling(self):
        """Test jfpv1 primitive boolean handling.

        Verify that:
        - Booleans are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        none_val = None
        none_out_raw = jfp._flatten_json(data=none_val)
        expected_bool_out_raw = [{'path': '', 'value': none_val}]
        self.assertEqual(none_out_raw, expected_bool_out_raw)
        bool_fp = jfp.json_fingerprint(input=json.dumps(none_val), hash_function='sha256', version=1)
        self.assertEqual(bool_fp, 'jfpv1$sha256$83e59f6a083bae820546809fbd4c91b79dc35e4c503c58c1c7950c1f7265af8d')

    def test_jfpv1_flattened_json_sibling_format(self):
        """Test jfpv1 json flattener.

        Verify that:
        - jfpv1 json flattener produces expected raw output format (non-hashed siblings in debug mode)
        - jfpv1 json flattener produces expected standard output format (hashed siblings)"""
        obj_in = [
            1,
            [2, 3],
        ]
        obj_out_raw = jfp._flatten_json(data=obj_in, debug=True)
        expected_obj_out_raw = [
            {
                'path': '[2]',
                'siblings': [
                    {'path': '[2]', 'value': 1},
                    {
                        'path': '[2]|[2]',
                        'siblings': [
                            {'path': '[2]|[2]', 'value': 2},
                            {'path': '[2]|[2]', 'value': 3}
                        ],
                        'value': 2
                    },
                    {
                        'path': '[2]|[2]',
                        'siblings': [
                            {'path': '[2]|[2]', 'value': 2},
                            {'path': '[2]|[2]', 'value': 3}
                        ],
                        'value': 3
                    }
                ],
                'value': 1
            },
            {
                'path': '[2]|[2]',
                'siblings': [
                    {'path': '[2]|[2]', 'value': 2},
                    {'path': '[2]|[2]', 'value': 3}
                ],
                'value': 2
            },
            {
                'path': '[2]|[2]',
                'siblings': [
                    {'path': '[2]|[2]', 'value': 2},
                    {'path': '[2]|[2]', 'value': 3}
                ],
                'value': 3
            },
        ]
        self.assertEqual(obj_out_raw, expected_obj_out_raw)

        obj_out = jfp._flatten_json(data=obj_in, debug=False)
        inner_list_siblings_hash_list = jfp._create_sorted_sha256_hash_list([
            {'path': '[2]|[2]', 'value': 2},
            {'path': '[2]|[2]', 'value': 3}
        ])
        siblings_1 = jfp._create_sorted_sha256_hash_list([
            {'path': '[2]', 'value': 1},
            {
                'path': '[2]|[2]',
                'siblings': jfp._create_json_sha256_hash(inner_list_siblings_hash_list),
                'value': 2
            },
            {
                'path': '[2]|[2]',
                'siblings': jfp._create_json_sha256_hash(inner_list_siblings_hash_list),
                'value': 3
            }
        ])
        expected_out_hash_lists = [
            {
                'path': '[2]',
                'siblings': jfp._create_json_sha256_hash(siblings_1),
                'value': 1
            },
            {
                'path': '[2]|[2]',
                'siblings': jfp._create_json_sha256_hash(inner_list_siblings_hash_list),
                'value': 2
            },
            {
                'path': '[2]|[2]',
                'siblings': jfp._create_json_sha256_hash(inner_list_siblings_hash_list),
                'value': 3
            },
        ]
        self.assertEqual(obj_out, expected_out_hash_lists)

    def test_jfpv1_flattened_json_structural_distinction_1(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Identical value content in identical depths, but in different structures,
          don't produce identical outputs"""
        obj_in_1 = [
            1,
            [1, [2, 2]],
            [2, [2, 2]],
        ]
        fp_1 = jfp.json_fingerprint(input=json.dumps(obj_in_1), hash_function='sha256', version=1)

        obj_in_2 = [
            1,
            [1, 2, [2, 2, 2, 2]],
        ]
        fp_2 = jfp.json_fingerprint(input=json.dumps(obj_in_2), hash_function='sha256', version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_flattened_json_structural_distinction_2(self):
        """Test jfpv1 json flattener's structural value distinction.

        Verify that:
        - Values in identical paths but different sibling values don't get matched"""
        obj_in_1 = [
            [1, ['x', 'x']],
            [2, ['y', 'y']],
        ]
        fp_1 = jfp.json_fingerprint(input=json.dumps(obj_in_1), hash_function='sha256', version=1)

        obj_in_2 = [
            [1, ['x', 'y']],
            [2, ['x', 'y']],
        ]
        fp_2 = jfp.json_fingerprint(input=json.dumps(obj_in_2), hash_function='sha256', version=1)

        self.assertNotEqual(fp_1, fp_2)


if __name__ == '__main__':
    unittest.main()

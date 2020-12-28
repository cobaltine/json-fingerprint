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
        expected_int_out_raw = [{'path': '', 'siblings': [], 'value': int_val}]
        self.assertEqual(int_out_raw, expected_int_out_raw)
        int_fp = jfp.json_fingerprint(input=json.dumps(int_val), hash_function='sha256', version=1)
        self.assertEqual(int_fp, 'jfpv1$sha256$16096dbc64a551bd3ab7fde9935338b3575b8c1e1e371b9af7765b7d8fb5ccc5')

    def test_jfpv1_sha256_primitive_float_handling(self):
        """Test jfpv1 primitive float handling.

        Verify that:
        - Floats are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        float_val = 123.321
        float_out_raw = jfp._flatten_json(data=float_val)
        expected_float_out_raw = [{'path': '', 'siblings': [], 'value': float_val}]
        self.assertEqual(float_out_raw, expected_float_out_raw)
        float_fp = jfp.json_fingerprint(input=json.dumps(float_val), hash_function='sha256', version=1)
        self.assertEqual(float_fp, 'jfpv1$sha256$33755cda351618d316af2661b9e9a5c87123b715898662b50837b8079135bfbb')

    def test_jfpv1_sha256_primitive_string_handling(self):
        """Test jfpv1 primitive string handling.

        Verify that:
        - Strings are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        string_val = 'alpha 123'
        string_out_raw = jfp._flatten_json(data=string_val)
        expected_string_out_raw = [{'path': '', 'siblings': [], 'value': string_val}]
        self.assertEqual(string_out_raw, expected_string_out_raw)
        string_fp = jfp.json_fingerprint(input=json.dumps(string_val), hash_function='sha256', version=1)
        self.assertEqual(string_fp, 'jfpv1$sha256$4d1da719b6f0845aa4a4036150322f76d03f0781dadab388d858d45a881a4e24')

    def test_jfpv1_sha256_primitive_boolean_handling(self):
        """Test jfpv1 primitive boolean handling.

        Verify that:
        - Booleans are 'flattened' correctly (path, siblings and value)
        - Fingerprint matches with pre-verified fingerprint"""
        bool_val = True
        bool_out_raw = jfp._flatten_json(data=bool_val)
        expected_bool_out_raw = [{'path': '', 'siblings': [], 'value': bool_val}]
        self.assertEqual(bool_out_raw, expected_bool_out_raw)
        bool_fp = jfp.json_fingerprint(input=json.dumps(bool_val), hash_function='sha256', version=1)
        self.assertEqual(bool_fp, 'jfpv1$sha256$ffd2ec80a46b8035bd07c380548e62deaf730c2822c72e7c2fe690b4928f80cd')

    def test_jfpv1_flattened_json_sibling_format(self):
        """Test jfpv1 json flattener.

        Verify that:
        - jfpv1 json flattener produces expected raw output format (non-hashed siblings in debug mode)
        - jfpv1 json flattener produces expected output format (hashed siblings)"""
        obj_in = [
            1,
            [2, 3],
        ]

        obj_out_raw = jfp._flatten_json(data=obj_in, debug=True)

        expected_obj_out_raw = [
            {
                'path': '[2]',
                'siblings': [
                    {'path': '[2]', 'siblings': [], 'value': 1},
                    {
                        'path': '[2]|[2]',
                        'siblings': [
                            {'path': '[2]|[2]', 'siblings': [], 'value': 2},
                            {'path': '[2]|[2]', 'siblings': [], 'value': 3}
                        ],
                        'value': 2
                    },
                    {
                        'path': '[2]|[2]',
                        'siblings': [
                            {'path': '[2]|[2]', 'siblings': [], 'value': 2},
                            {'path': '[2]|[2]', 'siblings': [], 'value': 3}
                        ],
                        'value': 3
                    }
                ],
                'value': 1
            },
            {
                'path': '[2]|[2]',
                'siblings': [
                    {'path': '[2]|[2]', 'siblings': [], 'value': 2},
                    {'path': '[2]|[2]', 'siblings': [], 'value': 3}
                ],
                'value': 2
            },
            {
                'path': '[2]|[2]',
                'siblings': [
                    {'path': '[2]|[2]', 'siblings': [], 'value': 2},
                    {'path': '[2]|[2]', 'siblings': [], 'value': 3}
                ],
                'value': 3
            },
        ]
        self.assertEqual(obj_out_raw, expected_obj_out_raw)

        obj_out = jfp._flatten_json(data=obj_in, debug=False)
        expected_obj_out = [
            {
                'path': '[2]',
                'siblings': ['5e557218f2a8ede068df419cb0e262ae6cec8ef2f3725ee3f93aa5b37cae8faa',
                             '88100b1653088080ff37e8483ac553592c6ad7162f0225f61470d30db242e217',
                             'c171006637945ce8acd13c6c085a61f219c1dfef40952dd62be30b41a611e5ae'],
                'value': 1
            },
            {
                'path': '[2]|[2]',
                'siblings': ['0e956de640eb3f36ce14d102f309353351a9f18ce6bb6aeff498453f7fb711de',
                             'bcf8a66b0b67203a6724f642d9ab894c3a767619ed053db975ac560e7618ec35'],
                'value': 2
            },
            {
                'path': '[2]|[2]',
                'siblings': ['0e956de640eb3f36ce14d102f309353351a9f18ce6bb6aeff498453f7fb711de',
                             'bcf8a66b0b67203a6724f642d9ab894c3a767619ed053db975ac560e7618ec35'],
                'value': 3
            },
        ]
        self.assertEqual(obj_out, expected_obj_out)

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


if __name__ == '__main__':
    unittest.main()

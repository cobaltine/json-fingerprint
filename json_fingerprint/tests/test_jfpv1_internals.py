import hashlib
import json
import json_fingerprint as jfp
import unittest


class TestJsonFingerprint(unittest.TestCase):
    def test_jfpv1_sha256_output_format(self):
        """Test jfpv1 output format.

        Verify that:
        - Complete jfpv1-sha256 output fingerprint is properly formatted"""
        fp = jfp.json_fingerprint('{"foo": "bar"}', hash_function='sha256', version=1)
        self.assertRegex(fp, '^jfpv1\\$sha256\\$[0-9a-f]{64}$')

    def test_jfpv1_flattened_json_sibling_format(self):
        """Test jfpv1 json flattener.

        Verify that:
        - jfpv1 json flattener produces expected raw output format (non-hashed siblings)
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
        """Test jfpv1 json flattener depth handling.

        Verify that:
        - Identical value content in different structures (depths) don't prodcue same outputs"""
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
        """Test jfpv1 json flattener element distribution distinction.

        Verify that:
        - Values in identical paths but different sibling values don't get matched"""
        obj_in_1 = [
            [1, ["x", "x"]],
            [2, ["y", "y"]],
        ]
        fp_1 = jfp.json_fingerprint(input=json.dumps(obj_in_1), hash_function='sha256', version=1)

        obj_in_2 = [
            [1, ["x", "y"]],
            [2, ["x", "y"]],
        ]
        fp_2 = jfp.json_fingerprint(input=json.dumps(obj_in_2), hash_function='sha256', version=1)

        self.assertNotEqual(fp_1, fp_2)

    def test_jfpv1_create_sorted_hash_list(self):
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

        output_data_hashes = jfp._create_sorted_hash_list(data=input_data)

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

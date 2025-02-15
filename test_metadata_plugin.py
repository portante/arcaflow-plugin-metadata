#!/usr/bin/env python3
import unittest
import metadata_plugin
from arcaflow_plugin_sdk import plugin


class HelloWorldTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(metadata_plugin.InputParams())

        plugin.test_object_serialization(
            metadata_plugin.SuccessOutput(
                metadata={
                    "env": {
                        "SHELL": "/bin/bash",
                    },
                    "system": "linux",
                    "processor_count": 1,
                    "system_capabilities": [],
                }
            )
        )

        plugin.test_object_serialization(
            metadata_plugin.ErrorOutput(error="This is an error")
        )

    def test_functional(self):
        input = metadata_plugin.InputParams()

        output_id, output_data = metadata_plugin.collect_metadata(input)

        self.assertEqual("success", output_id)
        self.assertIsInstance(output_data.metadata, dict)
        self.assertGreaterEqual(len(output_data.metadata), 1)
        # Some expected keys in the dict
        self.assertTrue("env" in output_data.metadata)
        self.assertTrue("distribution" in output_data.metadata)

    def test_convert_to_homogeneous_list(self):
        test_cases = [
            ["a", "b", "c"],  # all str
            ["a", "b", 1],  # One final int to convert to str
            [1.0, 1, "1"],  # str at end, so upconvert all to str
            ["1", 1, 1.0],
            ["1", 1, 1],
            [1, 1, "1"],
            [1, 1, 1],
            [1.0, 1, 1],
            [1, 1, 1.0],
        ]
        # Ensure they're all homogeneous
        for test_case in test_cases:
            validate_list_items_homogeous_type(
                self, metadata_plugin.convert_to_homogenous_list(test_case)
            )
        # Ensure the type matches
        self.assertEqual(
            int, type(metadata_plugin.convert_to_homogenous_list([1, 1, 1])[0])
        )
        self.assertEqual(
            float, type(metadata_plugin.convert_to_homogenous_list([1, 1, 1.0])[0])
        )
        self.assertEqual(
            str, type(metadata_plugin.convert_to_homogenous_list([1, 1.0, "1.0"])[0])
        )


def validate_list_items_homogeous_type(t, input_list):
    if len(input_list) == 0:
        return  # no problem with an empty list
    expected_type = type(input_list[0])
    for item in input_list:
        t.assertEqual(type(item), expected_type)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

"""
Copyright 2024 carlkidcrypto, All rights reserved.
"""

import unittest
import sys

sys.path.append("../")

from purpleair_api.PurpleAirAPIConstants import (
    PRINT_DEBUG_MSGS,
    ERROR_CODES_LIST,
    SUCCESS_CODE_LIST,
    ACCEPTED_FIELD_NAMES_DICT,
)


class PurpleAirAPIConstantsTest(unittest.TestCase):
    def test_print_debug_msgs_is_false(self):
        """
        Test that PRINT_DEBUG_MSGS defaults to False.
        """
        self.assertFalse(PRINT_DEBUG_MSGS)

    def test_error_codes_list_is_list(self):
        """
        Test that ERROR_CODES_LIST is a list and contains expected HTTP error codes.
        """
        self.assertIsInstance(ERROR_CODES_LIST, list)
        self.assertIn(400, ERROR_CODES_LIST)
        self.assertIn(403, ERROR_CODES_LIST)
        self.assertIn(404, ERROR_CODES_LIST)

    def test_success_codes_list_is_list(self):
        """
        Test that SUCCESS_CODE_LIST is a list and contains expected HTTP success codes.
        """
        self.assertIsInstance(SUCCESS_CODE_LIST, list)
        self.assertIn(200, SUCCESS_CODE_LIST)
        self.assertIn(201, SUCCESS_CODE_LIST)

    def test_error_and_success_codes_are_disjoint(self):
        """
        Test that no code appears in both ERROR_CODES_LIST and SUCCESS_CODE_LIST.
        """
        overlap = set(ERROR_CODES_LIST) & set(SUCCESS_CODE_LIST)
        self.assertEqual(len(overlap), 0)

    def test_accepted_field_names_dict_is_dict(self):
        """
        Test that ACCEPTED_FIELD_NAMES_DICT is a dict with string keys.
        """
        self.assertIsInstance(ACCEPTED_FIELD_NAMES_DICT, dict)
        self.assertGreater(len(ACCEPTED_FIELD_NAMES_DICT), 0)
        for key in ACCEPTED_FIELD_NAMES_DICT:
            self.assertIsInstance(key, str)

    def test_accepted_field_names_dict_contains_core_fields(self):
        """
        Test that ACCEPTED_FIELD_NAMES_DICT contains expected sensor fields.
        """
        expected_fields = ["name", "latitude", "longitude", "humidity", "temperature"]
        for field in expected_fields:
            self.assertIn(field, ACCEPTED_FIELD_NAMES_DICT)


if __name__ == "__main__":
    unittest.main()

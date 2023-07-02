#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import sys

sys.path.append("../")

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError


class PurpleAirAPIErrorTest(unittest.TestCase):
    def setUp(self):
        self.error_msg_str = ""

    def tearDown(self):
        self.error_msg_str = ""

    def test_custom_error(self):
        """
        Test that our custom error is called PurpleAirAPIError
        """

        # Setup
        self.error_msg_str = "This is a test!"

        # Action
        retval = PurpleAirAPIError(self.error_msg_str)

        # Expected Result
        self.assertEqual(retval.message, self.error_msg_str)
        self.assertEqual(retval.__class__, PurpleAirAPIError)


if __name__ == "__main__":
    unittest.main()

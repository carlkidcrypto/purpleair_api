#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""

import unittest
import sys

sys.path.append("../")

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError


class PurpleAirAPIErrorTest(unittest.TestCase):
    def test_custom_error(self):
        """
        Test that our custom error is called PurpleAirAPIError
        """

        # Setup
        error_msg_str = "This is a test!"

        # Action
        retval = PurpleAirAPIError(error_msg_str)

        # Expected Result
        self.assertEqual(retval.message, error_msg_str)
        self.assertIsInstance(retval, PurpleAirAPIError)

    def test_custom_error_is_exception(self):
        """
        Test that PurpleAirAPIError is a subclass of Exception.
        """
        self.assertTrue(issubclass(PurpleAirAPIError, Exception))

    def test_custom_error_can_be_raised_and_caught(self):
        """
        Test that PurpleAirAPIError can be raised and caught as an Exception.
        """
        error_msg_str = "raise and catch test"

        with self.assertRaises(PurpleAirAPIError) as ctx:
            raise PurpleAirAPIError(error_msg_str)

        self.assertEqual(ctx.exception.message, error_msg_str)

    def test_custom_error_str_representation(self):
        """
        Test that str() of PurpleAirAPIError returns the message string.
        """
        error_msg_str = "string representation test"
        error = PurpleAirAPIError(error_msg_str)
        self.assertEqual(str(error), error_msg_str)


if __name__ == "__main__":
    unittest.main()

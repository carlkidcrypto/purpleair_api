#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
"""




import unittest
from io import StringIO
import sys
sys.path.append("../") 

from purpleair_api.PurpleAirAPIConstants import PRINT_DEBUG_MSGS
from purpleair_api.PurpleAirAPIHelpers import *

class PurpleAirAPIHelpersTest(unittest.TestCase):
    def setUp(self):
        self.msg_str = ""
        self.out = StringIO()

    def tearDown(self):
         self.msg_str = ""
         self.out.close()

    def test_debug_log_global_flag_false(self):
        """
        Test that no debug messages are printed when PRINT_DEBUG_MSGS is `false`
        """

        # Setup
        globals()["PRINT_DEBUG_MSGS"] = False
        self.msg_str = "this is a test debug message!"

        # Action
        debug_log(self.msg_str)

        # Expected Result
        self.assertEqual("", self.out.getvalue())

    def test_debug_log_global_flag_true(self):
        """
        Test that debug messages are printed when PRINT_DEBUG_MSGS is `true`
        """

        # Setup
        globals()["PRINT_DEBUG_MSGS"] = True
        self.msg_str = "this is a test debug message!"

        # Action
        debug_log(self.msg_str)

        # Expected Result
        self.assertEqual(self.msg_str,  self.out.getvalue())


if __name__ == "__main__":
    unittest.main()

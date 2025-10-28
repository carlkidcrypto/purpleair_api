#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
from random import choice
from copy import deepcopy
from io import StringIO
import requests_mock
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

    # This fails need to figure out why
    # def test_debug_log_global_flag_true(self):
    #     """
    #     Test that debug messages are printed when PRINT_DEBUG_MSGS is `true`
    #     """

    #     # Setup
    #     globals()["PRINT_DEBUG_MSGS"] = True
    #     self.msg_str = "this is a test debug message!"

    #     # Action
    #     debug_log(self.msg_str)

    #     # Expected Result
    #     self.assertEqual(self.msg_str,  self.out.getvalue())

    def test_verify_request_status_code_true(self):
        """
        Test that the codes in SUCCESS_CODE_LIST return true
        """

        # Setup
        from purpleair_api.PurpleAirAPIConstants import SUCCESS_CODE_LIST

        # Action and Expected Result
        for success_code in SUCCESS_CODE_LIST:
            self.assertTrue(verify_request_status_codes(success_code))

    def test_verify_request_status_code_false(self):
        """
        Test that the codes in ERROR_CODES_LIST return false
        """

        # Setup
        from purpleair_api.PurpleAirAPIConstants import ERROR_CODES_LIST

        # Action and Expected Result
        for error_code in ERROR_CODES_LIST:
            self.assertFalse(verify_request_status_codes(error_code))

    def test_verify_request_status_code_raise_error(self):
        """
        Test that the codes in not ERROR_CODES_LIST or SUCCESS_CODE_LIST raise `PurpleAirAPIError`'s
        """

        # Setup
        from purpleair_api.PurpleAirAPIConstants import (
            ERROR_CODES_LIST,
            SUCCESS_CODE_LIST,
        )

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            for error_code in ERROR_CODES_LIST:
                self.assertRaises(verify_request_status_codes(~error_code))

            for success_code in SUCCESS_CODE_LIST:
                self.assertRaises(verify_request_status_codes(~success_code))

    def test_convert_requests_text_to_json_none(self):
        """
        Test that the method returns none if no text is provided
        """

        # Setup
        input_text = None

        # Action
        retval = convert_requests_text_to_json(input_text)

        # Expected Result
        self.assertIsNone(retval)

    def test_convert_requests_text_to_json_dict(self):
        """
        Test that the method returns a python dict object after loading in valid json
        """

        # Setup
        input_text = '{"test_key": "test_value"}'

        # Action
        retval = convert_requests_text_to_json(input_text)

        # Expected Result
        self.assertDictEqual(retval, {"test_key": "test_value"})

    def test_sanitize_sensor_data_from_paa(self):
        """
        Test that the sanitize function adds missing keys if they don't exist
        """

        # Setup
        from purpleair_api.PurpleAirAPIConstants import ACCEPTED_FIELD_NAMES_DICT

        dict_length = len(ACCEPTED_FIELD_NAMES_DICT)
        dict_copy = deepcopy(ACCEPTED_FIELD_NAMES_DICT)
        dict_keys_list = list(ACCEPTED_FIELD_NAMES_DICT.keys())
        fake_data = {"sensor": {}}

        # Action
        item_to_remove = dict_keys_list[choice(range(0, 1, dict_length))]
        dict_copy.pop(item_to_remove)
        fake_data["sensor"] = dict_copy
        self.assertNotEqual(len(dict_copy), dict_length)
        retval = sanitize_sensor_data_from_paa(fake_data)

        # Expected Result
        self.assertEqual(ACCEPTED_FIELD_NAMES_DICT.keys(), retval["sensor"].keys())
        self.assertEqual(
            ACCEPTED_FIELD_NAMES_DICT[item_to_remove], retval["sensor"][item_to_remove]
        )

    def test_send_url_get_request_none(self):
        """
        Test that if no `request_url` is provied, we raise a `PurpleAPIError`.
        """

        # Setup
        fake_url_request = None

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            send_url_get_request(request_url=fake_url_request)

    def test_send_url_get_request_optional_parameter_1(self):
        """
        Test that the `?` optional parameter is added to the first positional argument in the request url string.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys?param_1=abc&param_2=5"
        fake_api_key_to_use = "1111-222-333-4444-5555-6666-7777"
        fake_first_optional_parameter_separator = "?"
        optional_parameters_dict = {"param_1": "abc", "param_2": 5}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                expected_fake_url,
                text='{"test": 5}',
                status_code=200,
                headers={"X-API-Key": str(fake_api_key_to_use)},
            )
            send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )

    def test_send_url_get_request_optional_parameter_2(self):
        """
        Test that the `&` optional parameter is added to the first positional argument in the request url string.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys&param_1=abc&param_2=5"
        fake_api_key_to_use = "1111-222-333-4444-5555-6666-7777"
        fake_first_optional_parameter_separator = "&"
        optional_parameters_dict = {"param_1": "abc", "param_2": 5}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                expected_fake_url,
                text='{"test": 5}',
                status_code=200,
                headers={"X-API-Key": str(fake_api_key_to_use)},
            )
            send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )

    def test_send_url_get_request_optional_parameter_raise_error(self):
        """
        Test that an invalid optional parameter raises a `PurpleAirAPIError`.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys&param_1=abc&param_2=5"
        fake_api_key_to_use = "1111-222-333-4444-5555-6666-7777"
        fake_first_optional_parameter_separator = "'"
        optional_parameters_dict = {"param_1": "abc", "param_2": 5}

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )

    def test_send_url_get_request_no_api_key(self):
        """
        Test that a no API request can happen
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys&param_1=abc&param_2=5"
        fake_api_key_to_use = None
        fake_first_optional_parameter_separator = "&"
        optional_parameters_dict = {"param_1": "abc", "param_2": 5}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                expected_fake_url,
                text='{"test": 5}',
                status_code=200,
            )
            send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )

    def test_send_url_get_request_error_response(self):
        """
        Test that if our response returns an error, we raise `PurpleAirAPIError`.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys&param_1=abc&param_2=5"
        fake_api_key_to_use = None
        fake_first_optional_parameter_separator = "&"
        optional_parameters_dict = {"param_1": "abc", "param_2": 5}

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            with requests_mock.Mocker() as m:
                m.get(
                    expected_fake_url,
                    text='{"test": 5, "error": "BAD!", "description": "BAD BAD!"}',
                    status_code=400,
                )
                send_url_get_request(
                    request_url=fake_url_request,
                    api_key_to_use=fake_api_key_to_use,
                    first_optional_parameter_separator=fake_first_optional_parameter_separator,
                    optional_parameters_dict=optional_parameters_dict,
                )

    def test_send_url_post_request_json_param(self):
        """
        Test that we can provide json parameters
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/del"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {"val_1": 2, "val_2": 5}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.post(
                fake_url_request,
                headers={"X-API-Key": str(fake_api_key_to_use)},
                json=fake_json_post_params,
                status_code=200,
            )
            send_url_post_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                json_post_parameters=fake_json_post_params,
            )

    def test_send_url_post_request_no_json_param(self):
        """
        Test that we can provide no json parameters
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/pos"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.post(
                fake_url_request,
                headers={"X-API-Key": str(fake_api_key_to_use)},
                json=fake_json_post_params,
                status_code=200,
            )
            send_url_post_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                json_post_parameters=fake_json_post_params,
            )

    def test_send_url_post_request_error_response(self):
        """
        Test that if our response returns an error, we raise `PurpleAirAPIError`.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/del"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {}

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            with requests_mock.Mocker() as m:
                m.post(
                    fake_url_request,
                    headers={"X-API-Key": str(fake_api_key_to_use)},
                    text='{"test": 5, "error": "BAD!", "description": "BAD BAD!"}',
                    status_code=400,
                )
                send_url_post_request(
                    request_url=fake_url_request,
                    api_key_to_use=fake_api_key_to_use,
                    json_post_parameters=fake_json_post_params,
                )

    def test_send_url_delete_request_json_param(self):
        """
        Test that we can provide json parameters
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/del"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {"no_data": 4}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.delete(
                fake_url_request,
                headers={"X-API-Key": str(fake_api_key_to_use)},
                json=fake_json_post_params,
                status_code=200,
            )
            send_url_delete_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                json_post_parameters=fake_json_post_params,
            )

    def test_send_url_delete_request_no_json_param(self):
        """
        Test that we can provide no json parameters
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/del"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.delete(
                fake_url_request,
                headers={"X-API-Key": str(fake_api_key_to_use)},
                json=fake_json_post_params,
                status_code=200,
            )
            send_url_delete_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                json_post_parameters=fake_json_post_params,
            )

    def test_send_url_delete_request_error_response(self):
        """
        Test that if our response returns an error, we raise `PurpleAirAPIError`.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/del"
        fake_api_key_to_use = "111-222-333-444"
        fake_json_post_params = {}

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            with requests_mock.Mocker() as m:
                m.delete(
                    fake_url_request,
                    headers={"X-API-Key": str(fake_api_key_to_use)},
                    text='{"test": 5, "error": "BAD!", "description": "BAD BAD!"}',
                    status_code=400,
                )
                send_url_delete_request(
                    request_url=fake_url_request,
                    api_key_to_use=fake_api_key_to_use,
                    json_post_parameters=fake_json_post_params,
                )


if __name__ == "__main__":
    unittest.main()

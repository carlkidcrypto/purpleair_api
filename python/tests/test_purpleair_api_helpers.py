#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""

import unittest
from random import choice
from copy import deepcopy
from unittest.mock import patch
import requests_mock
import sys

sys.path.append("../")

import purpleair_api.PurpleAirAPIHelpers as helpers_module
from purpleair_api.PurpleAirAPIHelpers import *


class PurpleAirAPIHelpersTest(unittest.TestCase):
    def test_debug_log_no_exception(self):
        """
        Test that debug_log doesn't raise an exception when called
        """
        # Setup
        msg_str = "this is a test debug message!"

        # Action and Expected Result - No exception should be raised
        try:
            debug_log(msg_str)
        except Exception as e:
            self.fail(f"debug_log raised an exception: {e}")

    def test_debug_log_prints_when_enabled(self):
        """
        Test that debug_log prints a message when PRINT_DEBUG_MSGS is True
        """
        # Setup
        msg_str = "debug enabled message"

        # Action and Expected Result - patch PRINT_DEBUG_MSGS to True and verify print is called
        with patch.object(helpers_module, "PRINT_DEBUG_MSGS", True):
            with patch("builtins.print") as mock_print:
                debug_log(msg_str)
                mock_print.assert_called_once_with("\033[1;31m" + msg_str + "\x1b[0m")

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

        # Action - Remove a random key
        item_to_remove = dict_keys_list[choice(range(dict_length))]
        dict_copy.pop(item_to_remove)
        fake_data["sensor"] = dict_copy
        self.assertNotEqual(len(dict_copy), dict_length)
        retval = sanitize_sensor_data_from_paa(fake_data)

        # Expected Result - Verify missing key was added back
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

    def test_send_url_get_request_all_optional_params_none(self):
        """
        Test that when optional_parameters_dict has all None values the URL is unchanged.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        fake_api_key_to_use = "1111-222-333-4444-5555-6666-7777"
        fake_first_optional_parameter_separator = "?"
        optional_parameters_dict = {"param_1": None, "param_2": None}

        # Action and Expected Result — URL should not have any params appended
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            result = send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )
        self.assertEqual(result, {"test": 5})

    def test_send_url_get_request_single_non_none_optional_param(self):
        """
        Test that when optional_parameters_dict has exactly one non-None value,
        only that param is appended (exercises opt_param_count == 1 without hitting >= 2 branch).
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"
        expected_fake_url = "https://api.purpleair.com/v1/keys?only_param=hello"
        fake_api_key_to_use = "1111-222-333-4444"
        fake_first_optional_parameter_separator = "?"
        optional_parameters_dict = {"only_param": "hello", "missing_param": None}

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                expected_fake_url,
                text='{"result": 1}',
                status_code=200,
            )
            result = send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
                first_optional_parameter_separator=fake_first_optional_parameter_separator,
                optional_parameters_dict=optional_parameters_dict,
            )
        self.assertEqual(result, {"result": 1})

    def test_convert_requests_text_to_json_with_debug_enabled(self):
        """
        Test that convert_requests_text_to_json logs debug messages when PRINT_DEBUG_MSGS is True.
        """

        # Setup
        input_text = '{"debug_key": "debug_value"}'

        # Action and Expected Result — both debug_log calls inside the function should fire
        with patch.object(helpers_module, "PRINT_DEBUG_MSGS", True):
            with patch("builtins.print") as mock_print:
                result = convert_requests_text_to_json(input_text)
                self.assertEqual(mock_print.call_count, 2)

        self.assertDictEqual(result, {"debug_key": "debug_value"})

    def test_send_url_get_request_no_optional_params_dict(self):
        """
        Test that send_url_get_request works correctly when optional_parameters_dict is None
        (no optional params path — URL is sent as-is).
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/organization"
        fake_api_key_to_use = "test-key-123"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"org": "test"}',
                status_code=200,
            )
            result = send_url_get_request(
                request_url=fake_url_request,
                api_key_to_use=fake_api_key_to_use,
            )
        self.assertEqual(result, {"org": "test"})

    def test_send_url_get_request_strips_quotes_from_url(self):
        """
        Test that send_url_get_request strips embedded double-quotes from the URL
        before sending the request (exercises the request_url.replace('"', "") path).
        """

        # The URL after stripping should have no quotes
        cleaned_url = "https://api.purpleair.com/v1/sensors/1234"

        # Action and Expected Result — mocker registers the cleaned URL
        with requests_mock.Mocker() as m:
            m.get(
                cleaned_url,
                text='{"stripped": true}',
                status_code=200,
            )
            # Pass a URL that contains embedded quotes
            result = send_url_get_request(
                request_url='"https://api.purpleair.com/v1/sensors/1234"',
                api_key_to_use="testkey",
            )
        self.assertEqual(result, {"stripped": True})

    def test_send_url_get_request_strips_spaces_from_url(self):
        """
        Test that send_url_get_request strips whitespace from the URL
        before sending the request (exercises the request_url.replace(" ", "") path).
        """

        # The URL after stripping should have no spaces
        cleaned_url = "https://api.purpleair.com/v1/sensors/5678"

        # Action and Expected Result — mocker registers the cleaned URL
        with requests_mock.Mocker() as m:
            m.get(
                cleaned_url,
                text='{"stripped": true}',
                status_code=200,
            )
            # Pass a URL that contains spaces
            result = send_url_get_request(
                request_url="https://api.purpleair.com/v1/sensors/ 5678 ",
                api_key_to_use="testkey",
            )
        self.assertEqual(result, {"stripped": True})


if __name__ == "__main__":
    unittest.main()

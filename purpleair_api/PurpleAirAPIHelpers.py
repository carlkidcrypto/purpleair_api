#!/usr/bin/env python3

"""
    Copyright 2024 carlkidcrypto, All rights reserved.
    A python3 file containing helper functions for the PurpleAirAPI** files.
    https://api.purpleair.com/#api-welcome
"""

from purpleair_api.PurpleAirAPIConstants import (
    ACCEPTED_FIELD_NAMES_DICT,
    PRINT_DEBUG_MSGS,
    SUCCESS_CODE_LIST,
    ERROR_CODES_LIST,
)

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError
from requests import get, post, delete
from json import loads


def debug_log(debug_msg_string):
    """
    A helper function to print out
    debug messages only if DEBUG is defined as True in
    'PurpleAirAPIConstants.py'. Messages will be the color
    red.

    :param str debug_msg_string: The debug message string
    """

    if PRINT_DEBUG_MSGS:
        # Make debug messages red using ANSI escape code.
        print("\033[1;31m" + str(debug_msg_string) + "\x1b[0m")


def verify_request_status_codes(status_code) -> bool:
    """
    A helper to check those status codes.
    True if in SUCCESS_CODE_LIST
    False if in ERROR_CODES_LIST
    """

    if status_code in SUCCESS_CODE_LIST:
        return True

    elif status_code in ERROR_CODES_LIST:
        return False

    else:
        raise PurpleAirAPIError(f"Unkown status code - {status_code}!")


def convert_requests_text_to_json(text=None) -> dict:
    """
    A helper to convert request.text to json.

    :param str text: The request.txt to convert to json

    :return dict
    """

    the_request_text_as_json = None
    if text:
        debug_log(f"convert_requests_text_to_json - text: {text}")
        the_request_text_as_json = loads(text)
        debug_log(f"convert_requests_text_to_json - json: {the_request_text_as_json}")

    return the_request_text_as_json


def sanitize_sensor_data_from_paa(paa_return_data) -> dict:
    """
    A helper function.
    Since not all sensors support all field names we check that the keys exist
    in the sensor data. If they do not exist we add it in with a NULL
    equivalent. i.e 0.0, 0, "", etc.
    We access the "sensor" key inside this function.

    :param dict paa_return_data: A dictionary with paa return data
    """

    for key_str in ACCEPTED_FIELD_NAMES_DICT.keys():
        if key_str not in paa_return_data["sensor"].keys():
            paa_return_data["sensor"][key_str] = ACCEPTED_FIELD_NAMES_DICT[key_str]

    return paa_return_data


def send_url_get_request(
    request_url,
    api_key_to_use=None,
    first_optional_parameter_separator=None,
    optional_parameters_dict=None,
):
    """
    A helper to send the url request. It can also add onto the
    'request_url' string if 'optional_parameters_dict' are provided.

    :param str request_url: The constructed string url request string.
    :param str first_optional_parameter_separator: The separator between first parameter
                                                    in optional_parameters_dict. i.e '?' or '&'.
    :param dict optional_parameters_dict: Optional parameters that can be added onto the
                                            request_url.
    """

    if request_url is None:
        raise PurpleAirAPIError(f"A request URL string must be provided")

    if optional_parameters_dict is not None:
        if first_optional_parameter_separator not in ["?", "&"]:
            raise PurpleAirAPIError(
                f"Invalid `first_optional_parameter_separator: {first_optional_parameter_separator}` passed into `send_url_get_request`!"
            )

        opt_param_count = 0
        for opt_param, val in optional_parameters_dict.items():
            if val is not None:
                opt_param_count = opt_param_count + 1

                if opt_param_count == 1:
                    request_url = (
                        request_url
                        + f"{first_optional_parameter_separator}{opt_param}={str(val)}"
                    )

                elif opt_param_count >= 2:
                    request_url = request_url + f"&{opt_param}={str(val)}"

    # Strip any quotes that might persist
    request_url = request_url.replace('"', "")
    # Strip away any whitespace that might persist
    request_url = request_url.replace(" ", "")
    debug_log(request_url)
    my_request = None

    # If any API key is provided use it
    if api_key_to_use is not None:
        my_request = get(request_url, headers={"X-API-Key": str(api_key_to_use)})

    # No API key provided
    else:
        my_request = get(request_url)

    the_request_text_as_json = convert_requests_text_to_json(my_request.text)

    if verify_request_status_codes(my_request.status_code):
        my_request.close()
        del my_request
        return the_request_text_as_json

    else:
        raise PurpleAirAPIError(
            f"""{my_request.status_code}: {the_request_text_as_json['error']} - {the_request_text_as_json['description']}"""
        )


def send_url_post_request(request_url, api_key_to_use, json_post_parameters={}):
    """
    A class helper to send the url request. It can also add onto the
    'request_url' string if 'optional_parameters_dict' are provided.

    :param str request_url: The constructed string url request string.
    """

    debug_log(request_url)
    my_request = None
    if json_post_parameters:
        debug_log(json_post_parameters)
        my_request = post(
            request_url,
            headers={"X-API-Key": str(api_key_to_use)},
            json=json_post_parameters,
        )

    else:
        debug_log(json_post_parameters)
        my_request = post(request_url, headers={"X-API-Key": str(api_key_to_use)})

    the_request_text_as_json = convert_requests_text_to_json(my_request.text)

    if verify_request_status_codes(my_request.status_code):
        my_request.close()
        del my_request
        return the_request_text_as_json

    else:
        raise PurpleAirAPIError(
            f"""{my_request.status_code}: {the_request_text_as_json['error']} - {the_request_text_as_json['description']}"""
        )


def send_url_delete_request(request_url, api_key_to_use, json_post_parameters={}):
    """
    A class helper to send the url request. It can also add onto the
    'request_url' string if 'optional_parameters_dict' are provided.

    :param str request_url: The constructed string url request string.
    """

    debug_log(request_url)
    my_request = None
    if json_post_parameters:
        my_request = delete(
            request_url,
            headers={"X-API-Key": str(api_key_to_use)},
            json=json_post_parameters,
        )

    else:
        my_request = delete(request_url, headers={"X-API-Key": str(api_key_to_use)})

    the_request_text_as_json = convert_requests_text_to_json(my_request.text)

    if verify_request_status_codes(my_request.status_code):
        my_request.close()
        del my_request
        return the_request_text_as_json

    else:
        raise PurpleAirAPIError(
            f"""{my_request.status_code}: {the_request_text_as_json['error']} - {the_request_text_as_json['description']}"""
        )

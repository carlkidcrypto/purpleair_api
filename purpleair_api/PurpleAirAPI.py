#!/usr/bin/env python3

"""
    Copyright 2024 carlkidcrypto, All rights reserved.
    A python3 class designed to fetch data from Purple Air's new API.
    https://api.purpleair.com/#api-welcome
"""

from purpleair_api.PurpleAirAPIHelpers import debug_log, send_url_get_request
from purpleair_api.PurpleAirAPIError import PurpleAirAPIError
from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI
from purpleair_api.PurpleAirLocalAPI import PurpleAirLocalAPI


class PurpleAirAPI(PurpleAirReadAPI, PurpleAirWriteAPI, PurpleAirLocalAPI):
    """
    The PurpleAirAPI class designed to send valid
    PurpleAirAPI requests.
    """

    def __init__(
        self, your_api_read_key=None, your_api_write_key=None, your_ipv4_address=None
    ):
        """
        :param str your_api_read_key: A valid PurpleAirAPI Read key
        :param str your_api_write_key: A valid PurpleAirAPI Write key
        :param str your_ipv4_address: The IPv4 address of your PurpleAir.
        """

        # We can not have all three parameters be empty
        if (
            your_api_read_key is None
            and your_api_write_key is None
            and your_ipv4_address is None
        ):
            raise PurpleAirAPIError(
                "Ensure that the right combination of parameters have been provided! "
                + "`your_api_read_key` or `your_api_write_key` for external internet requests. Or "
                + "just `your_ipv4_address` for local network requests"
            )

        # Save off the API key for internal usage
        self._your_api_read_key = your_api_read_key

        self._base_api_v1_request_string = None

        # Create the base API request string. Must be HTTPS.
        if your_api_read_key or your_api_write_key:
            self._base_api_v1_request_string = "https://api.purpleair.com/v1/"

        # Place holders for information we care about
        self._api_versions = {}
        self._api_keys_last_checked = {}
        self._api_key_types = {}

        retval_api_read_key = None
        retval_api_write_key = None

        if your_api_read_key is not None:
            retval_api_read_key = self._check_an_api_key(your_api_read_key)

        if your_api_write_key is not None:
            retval_api_write_key = self._check_an_api_key(your_api_write_key)

        if your_ipv4_address is not None:
            PurpleAirLocalAPI.__init__(self, ipv4_address_list=your_ipv4_address)

        if retval_api_read_key is not None:
            if self._api_key_types[your_api_read_key] == "READ":
                PurpleAirWriteAPI.__init__(self, api_write_key=your_api_write_key)
                print("PurpleAirAPI: Successfully authenticated read key")

            else:
                raise PurpleAirAPIError("Ensure 'your_api_read_key' is a read key.")

        if retval_api_write_key is not None:
            if self._api_key_types[your_api_write_key] == "WRITE":
                PurpleAirReadAPI.__init__(self, api_read_key=your_api_read_key)
                print("PurpleAirAPI: Successfully authenticated write key")

            else:
                raise PurpleAirAPIError("Ensure 'your_api_write_key' is a write key")

        # Avoid logging sensitive API keys in debug output
        debug_log(f"_api_versions contains {len(self._api_versions)} key(s)")
        debug_log(f"_api_keys_last_checked contains {len(self._api_keys_last_checked)} key(s)")
        debug_log(f"_api_key_types contains {len(self._api_key_types)} key(s)")
        debug_log(your_ipv4_address)

    def _check_an_api_key(self, str_api_key_to_check):
        """
        An internal class helper method to check if an API key is valid.

        :param str str_api_key_to_check: A valid PurpleAirAPI key to check

        :return True, if an API key can be successfully verified.
        """
        request_url = self._base_api_v1_request_string + "keys"
        the_request_text_as_json = send_url_get_request(
            request_url, api_key_to_use=str_api_key_to_check
        )

        # We good :) get the request information
        self._api_versions[str_api_key_to_check] = the_request_text_as_json[
            "api_version"
        ]
        self._api_keys_last_checked[str_api_key_to_check] = the_request_text_as_json[
            "time_stamp"
        ]
        self._api_key_types[str_api_key_to_check] = the_request_text_as_json[
            "api_key_type"
        ]

        return True

    @property
    def get_api_versions(self):
        """
        A method to return the API versions being used for both read/write keys.
        """

        return self._api_versions

    @property
    def get_api_key_last_checked(self):
        """
        A method to return the timestamp of when the API read/write keys were last checked.
        """

        return self._api_keys_last_checked

    @property
    def get_api_key_type(self):
        """
        A method to return the API key types being used.
        """

        return self._api_key_types

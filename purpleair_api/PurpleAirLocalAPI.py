#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
    A python3 class designed to fetch data from Purple Air's new API.
    This class will handle all `local` requests
    https://api.purpleair.com/#api-welcome
"""

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError
from purpleair_api.PurpleAirAPIHelpers import send_url_get_request


class PurpleAirLocalAPI:
    """
    The PurpleAirLocalAPI class designed to send valid
    local network requests. It can work with one or many IPv4 addresses.

    :param list ipv4_address_list: A list of strings with valid IPv4 addresses for your sensors. The addresses don't need a CIDR.
    """

    def __init__(self, ipv4_address_list=None):
        # Create the vase API request string for local networks.
        error_msg = (
            "Must provide the IPv4 address list for the sensor(s) on your local network"
        )

        if type(ipv4_address_list) is type(None):
            raise PurpleAirAPIError(error_msg)

        elif type(ipv4_address_list) is not type(list()):
            raise PurpleAirAPIError(error_msg)

        for address in ipv4_address_list:
            if len(address) == 0 or len(address) > 15:
                raise PurpleAirAPIError(error_msg)

        self._base_api_local_network_request_string_dict = dict()
        for address in ipv4_address_list:
            self._base_api_local_network_request_string_dict[
                address
            ] = f"http://{address}/json"

    def request_local_sensor_data(self) -> dict:
        """
        A method to request a local sensors data. This sensor must be in a netork that is accessible
        """

        retval = {}
        for key, value in self._base_api_local_network_request_string_dict.items():
            request_value = send_url_get_request(value)
            retval[key] = request_value

        return retval

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
    local network requests.
    """

    def __init__(self, ipv4_address=None):
        # Create the vase API request string for local networks.
        error_msg = "Must provide the IPv4 address for the senson on your local network"

        if type(ipv4_address) is type(None):
            raise PurpleAirAPIError(error_msg)

        elif len(ipv4_address) == 0:
            raise PurpleAirAPIError(error_msg)

        self._base_api_local_network_request_string = f"http://{ipv4_address}/json"

    def request_local_sensor_data(self):
        """
        A method to request a local sensors data. This sensor must be in a netork that is accessible
        """

        return send_url_get_request(self._base_api_local_network_request_string)

#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import requests_mock
import sys

sys.path.append("../")

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError
from purpleair_api.PurpleAirLocalAPI import PurpleAirLocalAPI


class PurpleAirLocalAPITest(unittest.TestCase):
    def setUp(self):
        self.pala = PurpleAirLocalAPI(["192.168.1.2"])

    def tearDown(self):
        self.pala = None

    def test_request_local_sensor_data_ip_provided(self):
        """
        Test that we can provided a valid ip address. And that the url is formatted as expected.
        """

        # Setup
        fake_url_request = "http://192.168.1.2/json"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.pala.request_local_sensor_data()

    def test_request_local_sensor_data_none_ip_provided(self):
        """
        Test that providing no IP address results in a `PurpleAirAPIError`
        """

        # Setup,  Action, and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            self.pala = PurpleAirLocalAPI(None)

    def test_request_local_sensor_data_empty_list_ip_provided(self):
        """
        Test that providing no IP address results in a `PurpleAirAPIError`
        """

        # Setup,  Action, and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            self.pala = PurpleAirLocalAPI(None)

        with self.assertRaises(PurpleAirAPIError):
            self.pala = PurpleAirLocalAPI(["", ""])

        with self.assertRaises(PurpleAirAPIError):
            self.pala = PurpleAirLocalAPI({})


if __name__ == "__main__":
    unittest.main()

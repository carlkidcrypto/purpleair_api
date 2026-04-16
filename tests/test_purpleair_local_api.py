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

    def test_request_local_sensor_data_multiple_ips(self):
        """
        Test that we can request local sensor data from multiple IP addresses.
        """

        # Setup
        pala_multi = PurpleAirLocalAPI(["192.168.1.2", "192.168.1.3"])

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get("http://192.168.1.2/json", text='{"sensor": 1}', status_code=200)
            m.get("http://192.168.1.3/json", text='{"sensor": 2}', status_code=200)
            retval = pala_multi.request_local_sensor_data()

        self.assertIn("192.168.1.2", retval)
        self.assertIn("192.168.1.3", retval)


if __name__ == "__main__":
    unittest.main()

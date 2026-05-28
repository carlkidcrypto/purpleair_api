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

    def test_request_local_sensor_data_too_long_ip_provided(self):
        """
        Test that providing an IP address longer than 15 characters results in a `PurpleAirAPIError`.
        """

        # An address of 16 chars exercises the len(address) > 15 branch
        with self.assertRaises(PurpleAirAPIError):
            PurpleAirLocalAPI(["192.168.1.100000"])

    def test_request_local_sensor_data_multiple_ips(self):
        """
        Test that we can request data from multiple sensors at once.
        """

        # Setup
        pala = PurpleAirLocalAPI(["192.168.1.2", "192.168.1.3"])
        fake_url_1 = "http://192.168.1.2/json"
        fake_url_2 = "http://192.168.1.3/json"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(fake_url_1, text='{"sensor": 1}', status_code=200)
            m.get(fake_url_2, text='{"sensor": 2}', status_code=200)
            retval = pala.request_local_sensor_data()

        self.assertEqual(len(retval), 2)
        self.assertIn("192.168.1.2", retval)
        self.assertIn("192.168.1.3", retval)


if __name__ == "__main__":
    unittest.main()

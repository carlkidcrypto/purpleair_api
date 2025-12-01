#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import requests_mock
import sys

sys.path.append("../")

from purpleair_api.PurpleAirAPI import PurpleAirAPI, PurpleAirAPIError


class PurpleAirAPITest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_purpleairapi_valid_read_key(self):
        """
        Test that we can create a PurpleAirAPI with a valid read key
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 123456789, "api_key_type": "READ"}',
                status_code=200,
            )
            PurpleAirAPI(your_api_read_key="123456789")

    def test_purpleairapi_invalid_read_key(self):
        """
        Test that we can't create a PurpleAirAPI with an invalid read key
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 123456789, "api_key_type": "WRITE"}',
                status_code=200,
            )

            with self.assertRaises(PurpleAirAPIError):
                PurpleAirAPI(your_api_read_key="123456789")

    def test_purpleairapi_valid_write_key(self):
        """
        Test that we can create a PurpleAirAPI with a valid write key
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 123456789, "api_key_type": "WRITE"}',
                status_code=200,
            )
            PurpleAirAPI(your_api_write_key="123456789")

    def test_purpleairapi_invalid_write_key(self):
        """
        Test that we can't create a PurpleAirAPI with an invalid write key
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 123456789, "api_key_type": "READ"}',
                status_code=200,
            )

            with self.assertRaises(PurpleAirAPIError):
                PurpleAirAPI(your_api_write_key="123456789")

    def test_purpleairapi_with_no_args(self):
        """
        Test that we can't create a PurpleAirAPI with no args.
        """

        with self.assertRaises(PurpleAirAPIError):
            PurpleAirAPI()

    def test_purpleairapi_with_two_args(self):
        """
        Test that we can create a PurpleAirAPI with all three args.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 987654321, "api_key_type": "WRITE"}',
                status_code=200,
            )

            PurpleAirAPI(
                your_api_write_key="123456789", your_ipv4_address=["192.168.1.2"]
            )

        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 987654321, "api_key_type": "READ"}',
                status_code=200,
            )

            PurpleAirAPI(
                your_api_read_key="123456789", your_ipv4_address=["192.168.1.2"]
            )

    def test_purpleairapi_getters(self):
        """
        Test the PurpleAirAPI getters.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/keys"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"api_version" : "1.1.1", "time_stamp": 987654321, "api_key_type": "WRITE"}',
                status_code=200,
            )

            paa = PurpleAirAPI(your_api_write_key="123456789")

        self.assertEqual(paa.get_api_key_last_checked["123456789"], 987654321)
        self.assertEqual(paa.get_api_key_type["123456789"], "WRITE")
        self.assertEqual(paa.get_api_versions["123456789"], "1.1.1")


if __name__ == "__main__":
    unittest.main()

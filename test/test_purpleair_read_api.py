#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import requests_mock
import sys

sys.path.append("../")

from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI


class PurpleAirReadAPITest(unittest.TestCase):
    def setUp(self):
        self.pala = PurpleAirReadAPI(123456789)

    def tearDown(self):
        self.pala = None

    def test_request_sensor_data_with_no_optional_parameters(self):
        """
        Test that we can request a sensors data with no read key and no fields
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/1234"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.pala.request_sensor_data(1234)

    def test_request_sensor_data_with_read_key_no_fields(self):
        """
        Test that we can request a sensors data with a read key and no fields
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/1234?read_key=56789"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.pala.request_sensor_data(1234, 56789)

    def test_request_sensor_data_with_read_key_and_fields(self):
        """
        Test that we can request a sensors data with a read key and fields
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/1234?read_key=56789&fields=test1,test2,test3"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.pala.request_sensor_data(1234, 56789, "test1, test2, test3")

    def test_request_multiple_sensors_data_with_no_optional_parameters(self):
        """
        Test that we can request multiple sensors data with fields
        """

        # Setup
        fake_url_request = (
            "https://api.purpleair.com/v1/sensors/?fields=test1,test2,test3,test4,test5"
        )

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.pala.request_multiple_sensors_data("test1, test2, test3, test4, test5")

    # def test_request_sensor_historic_data(self):
    #     pass

    # def test_request_group_detail_data(self):
    #     pass

    # def test_request_member_data(self):
    #     pass

    # def test_request_member_historic_data(self):
    #     pass

    # def test_request_members_data(self):
    #     pass

    # def test_request_local_sensor_data_none_ip_provided(self):
    #     """
    #     Test that providing no IP address results in a `PurpleAirAPIError`
    #     """

    #     # Setup,  Action, and Expected Result
    #     with self.assertRaises(PurpleAirAPIError):
    #         self.pala = PurpleAirLocalAPI(None)

    # def test_request_local_sensor_data_empty_string_ip_provided(self):
    #     """
    #     Test that providing no IP address results in a `PurpleAirAPIError`
    #     """

    #     # Setup,  Action, and Expected Result
    #     with self.assertRaises(PurpleAirAPIError):
    #         self.pala = PurpleAirLocalAPI(None)

    #     with self.assertRaises(PurpleAirAPIError):
    #         self.pala = PurpleAirLocalAPI("")


if __name__ == "__main__":
    unittest.main()

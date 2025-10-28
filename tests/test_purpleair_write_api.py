#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import requests_mock
import sys

sys.path.append("../")

from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI


class PurpleAirWriteAPITest(unittest.TestCase):
    def setUp(self):
        self.pawa = PurpleAirWriteAPI(123456789)

    def tearDown(self):
        self.pawa = None

    def test_post_create_group_data(self):
        """
        Test that we can post to create a group for sensors.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.post(
                fake_url_request,
                text='{"test" : 1234}',
                status_code=200,
            )
            self.pawa.post_create_group_data("this_is_a_name")

    def test_post_create_member_with_sensor_index(self):
        """
        Test that we can post to add members to a sensor group.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/1234/members"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.post(
                fake_url_request,
                text='{"test" : 1234}',
                status_code=200,
            )
            self.pawa.post_create_member(group_id=1234, sensor_index=4567)


if __name__ == "__main__":
    unittest.main()

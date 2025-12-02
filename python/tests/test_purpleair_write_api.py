#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
"""


import unittest
import requests_mock
import sys

sys.path.append("../")

from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI
from purpleair_api.PurpleAirAPIError import PurpleAirAPIError


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

    def test_post_create_member_with_sensor_id(self):
        """
        Test that we can post to add members to a sensor group using sensor_id (option 1).
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
            self.pawa.post_create_member(group_id=1234, sensor_id="SENSOR123")

    def test_post_create_member_with_private_sensor(self):
        """
        Test that we can post to add a private sensor to a group (option 3).
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
            self.pawa.post_create_member(
                group_id=1234,
                sensor_id="SENSOR456",
                owner_email="test@example.com",
                location_type=0,
            )

    def test_post_create_member_with_invalid_params(self):
        """
        Test that invalid parameter combinations raise PurpleAirAPIError.
        """

        # Action and Expected Result
        with self.assertRaises(PurpleAirAPIError):
            # Both sensor_index and sensor_id provided
            self.pawa.post_create_member(
                group_id=1234, sensor_index=4567, sensor_id="SENSOR123"
            )

    def test_post_delete_group(self):
        """
        Test that we can delete a group.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/1234"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.delete(
                fake_url_request,
                text='{"success": true}',
                status_code=200,
            )
            self.pawa.post_delete_group(group_id=1234)

    def test_post_delete_member(self):
        """
        Test that we can delete a member from a group.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/1234/members/5678"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.delete(
                fake_url_request,
                text='{"success": true}',
                status_code=200,
            )
            self.pawa.post_delete_member(group_id=1234, member_id=5678)


if __name__ == "__main__":
    unittest.main()

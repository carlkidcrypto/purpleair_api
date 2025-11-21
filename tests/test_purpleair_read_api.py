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
        self.para = PurpleAirReadAPI(123456789)

    def tearDown(self):
        self.para = None

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
            self.para.request_sensor_data(1234)

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
            self.para.request_sensor_data(1234, 56789)

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
            self.para.request_sensor_data(1234, 56789, "test1, test2, test3")

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
            self.para.request_multiple_sensors_data(
                fields="test1, test2, test3, test4, test5"
            )

    def test_request_multiple_sensors_data_with_some_optional_parameters(self):
        """
        Test that we can request multiple sensors data with fields, location_type, show_only, max_age, nwlat, selat
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/?fields=test1,test2,test3,test4,test5&location_type=1&show_only=123,456&max_age=1234&nwlat=5678&selat=91234"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.para.request_multiple_sensors_data(
                fields="test1, test2, test3, test4, test5",
                location_type=1,
                show_only="123, 456",
                max_age=1234,
                nwlat=5678,
                selat=91234,
            )

    def test_request_multiple_sensors_data_with_all_optional_parameters(self):
        """
        Test that we can request multiple sensors data with fields, location_type, read_keys, show_only, modified_since, max_age, nwlng, nwlat, selng, & selat.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/?fields=test1,test2,test3,test4,test5&location_type=5&read_keys=asdf&show_only=124,567&modified_since=123456789&max_age=123456789&nwlng=123456&nwlat=6789&selng=444&selat=333"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.para.request_multiple_sensors_data(
                fields="test1, test2, test3, test4, test5",
                location_type=5,
                read_keys="asdf",
                show_only="124, 567",
                modified_since=123456789,
                max_age=123456789,
                nwlng=123456,
                nwlat=6789,
                selng=444,
                selat=333,
            )

    def test_request_sensor_historic_data_with_no_optional_parameters(self):
        """
        Test that we can request historic sensor data with no optional parameters. Just sensor_index and fields.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/1234/history?fields=name,field1,field2,etc"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.para.request_sensor_historic_data(
                sensor_index=1234,
                fields="name, field1, field2, etc",
            )

    def test_request_sensor_historic_data_with_csv_data_format_true(self):
        """
        Test that we can request historic csv sensor data with no optional parameters. Just sensor_index and fields.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/sensors/1234/history/csv?fields=name,field1,field2,etc"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.para.request_sensor_historic_data(
                sensor_index=1234,
                fields="name, field1, field2, etc",
                csv_data_format=True,
            )

    def test_request_organization_data(self):
        """
        Test that we can call the organization endpoint.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/organization"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 5}',
                status_code=200,
            )
            self.para.request_organization_data()

    def test_request_group_detail_data(self):

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/1234"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 500}',
                status_code=200,
            )
            self.para.request_group_detail_data(1234)

    def test_request_member_data(self):

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/4321/members/1234"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 500}',
                status_code=200,
            )
            self.para.request_member_data(4321, 1234)

    def test_request_member_historic_data(self):
        # Setup
        fake_url_request = (
            "https://api.purpleair.com/v1/groups/4321/members/1234/history/?fields=name"
        )

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 500}',
                status_code=200,
            )
            self.para.request_member_historic_data(4321, 1234, "name")

    def test_request_members_data(self):
        # Setup
        fake_url_request = (
            "https://api.purpleair.com/v1/groups/4321/members?fields=name"
        )

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"test": 500}',
                status_code=200,
            )
            self.para.request_members_data(4321, "name")

    def test_request_group_list_data(self):
        """
        Test that we can retrieve a list of all groups owned by the api_key.
        """

        # Setup
        fake_url_request = "https://api.purpleair.com/v1/groups/"

        # Action and Expected Result
        with requests_mock.Mocker() as m:
            m.get(
                fake_url_request,
                text='{"groups": [{"id": 1, "name": "Test Group"}]}',
                status_code=200,
            )
            self.para.request_group_list_data()


if __name__ == "__main__":
    unittest.main()

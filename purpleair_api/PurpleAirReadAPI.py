#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
    A python3 class designed to fetch data from Purple Air's new API.
    This class will handle all `read` requests
    https://api.purpleair.com/#api-welcome
"""

from purpleair_api.PurpleAirAPIHelpers import send_url_get_request


class PurpleAirReadAPI:
    """
    The PurpleAirReadAPI class designed to send valid
    read requests.
    """

    def __init__(self, api_read_key=None):
        # Save off the API key for internal usage
        self._your_api_read_key = api_read_key
        self._base_api_v1_request_string = "https://api.purpleair.com/v1/"

    def request_sensor_data(self, sensor_index, read_key=None, fields=None):
        """
        A method to retrieve sensor data from one sensor. Will return the
        response payload as a python dictionary.

        :param int sensor_index: The sensor_index as found in the JSON for
                                 this specific sensor.

        :param (optional) str read_key: This read_key is required for
                                        private devices. It is separate
                                        to the api_key and each sensor has
                                        its own read_key. Submit multiple
                                        keys by separating them with a
                                        comma (,) character for example:
                                        key-one,key-two,key-three.

        :param (optional) str fields: The 'Fields' parameter specifies which
                                      'sensor data fields' to include in the
                                      response. It is a comma separated list
                                      with one or more of the following:
                                      Refer to PurpleAir documentation for more
                                      information:
                                      https://api.purpleair.com/#api-sensors-get-sensor-data

        :return A python dictionary containing the payload response
        """

        request_url = self._base_api_v1_request_string + "sensors/" + f"{sensor_index}"

        optional_parameters_dict = {"read_key": read_key, "fields": fields}

        first_optional_parameter_separator = "?"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

    def request_multiple_sensors_data(
        self,
        fields,
        location_type=None,
        read_keys=None,
        show_only=None,
        modified_since=None,
        max_age=None,
        nwlng=None,
        nwlat=None,
        selng=None,
        selat=None,
    ):
        """
        A method to retrieve sensor data from multiple sensors. Will return the
        response payload as a python dictionary.

        :param str fields: The 'Fields' parameter specifies which 'sensor data fields' to include in the response. It is a comma separated list with one or more of the following:
                            Station information and status fields:
                            name, icon, model, hardware, location_type, private, latitude, longitude, altitude, position_rating, led_brightness, firmware_version, firmware_upgrade, rssi, uptime, pa_latency, memory, last_seen, last_modified, date_created, channel_state, channel_flags, channel_flags_manual, channel_flags_auto, confidence, confidence_manual, confidence_auto

                            Environmental fields:
                            humidity, humidity_a, humidity_b, temperature, temperature_a, temperature_b, pressure, pressure_a, pressure_b

                            Miscellaneous fields:
                            voc, voc_a, voc_b, ozone1, analog_input

                            PM1.0 fields:
                            pm1.0, pm1.0_a, pm1.0_b, pm1.0_atm, pm1.0_atm_a, pm1.0_atm_b, pm1.0_cf_1, pm1.0_cf_1_a, pm1.0_cf_1_b

                            PM2.5 fields:
                            pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5, pm2.5_a, pm2.5_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b

                            PM2.5 pseudo (simple running) average fields:
                            pm2.5_10minute, pm2.5_10minute_a, pm2.5_10minute_b, pm2.5_30minute, pm2.5_30minute_a, pm2.5_30minute_b, pm2.5_60minute, pm2.5_60minute_a, pm2.5_60minute_b, pm2.5_6hour, pm2.5_6hour_a, pm2.5_6hour_b, pm2.5_24hour, pm2.5_24hour_a, pm2.5_24hour_b, pm2.5_1week, pm2.5_1week_a, pm2.5_1week_b

                            PM10.0 fields:
                            pm10.0, pm10.0_a, pm10.0_b, pm10.0_atm, pm10.0_atm_a, pm10.0_atm_b, pm10.0_cf_1, pm10.0_cf_1_a, pm10.0_cf_1_b

                            Visibility fields:
                            scattering_coefficient, scattering_coefficient_a, scattering_coefficient_b, deciviews, deciviews_a, deciviews_b, visual_range, visual_range_a, visual_range_b

                            Particle count fields:
                            0.3_um_count, 0.3_um_count_a, 0.3_um_count_b, 0.5_um_count, 0.5_um_count_a, 0.5_um_count_b, 1.0_um_count, 1.0_um_count_a, 1.0_um_count_b, 2.5_um_count, 2.5_um_count_a, 2.5_um_count_b, 5.0_um_count, 5.0_um_count_a, 5.0_um_count_b, 10.0_um_count 10.0_um_count_a, 10.0_um_count_b

                            ThingSpeak fields, used to retrieve data from api.thingspeak.com:
                            primary_id_a, primary_key_a, secondary_id_a, secondary_key_a, primary_id_b, primary_key_b, secondary_id_b, secondary_key_b

        :param (optional) int location_type: The location_type of the sensors.
                                             Possible values are: 0 = Outside or 1 = Inside.

        :param (optional) str read_keys: A read_key is required for private devices. It is separate to the api_key and each sensor has its own read_key.
                                         Submit multiple keys by separating them with a comma (,) character for example: key-one,key-two,key-three

        :param (optional) str show_only: A comma (,) separated list of sensor_index values. When provided, the results are limited only to
                                         the sensors included in this list.

        :param (optional) str modified_since: The modified_since parameter causes only sensors modified after
                                              the provided time stamp to be included in the results. Using the
                                              time_stamp value from a previous call (recommended) will limit results
                                              to those with new values since the last request. Using a value of 0
                                              will match sensors modified at any time

        :param (optional) int max_age: Filter results to only include sensors modified or updated within the last
                                       number of seconds. Using a value of 0 will match sensors of any age.
                                       Default value: 604800

        :param (optional) int nwlng: A north west longitude for the bounding box. Use a bounding box to limit the sensors
                                     returned to a specific geographic area. The bounding box is defined by two points, a
                                     north west latitude/longitude and a south east latitude/longitude.

        :param (optional) int nwlat: A north west latitude for the bounding box.

        :param (optional) int selng: A south east longitude for the bounding box.

        :param (optional) int selat: A south east latitude for the bounding box.

        :return A python dictionary containing the payload response
        """

        request_url = (
            self._base_api_v1_request_string + "sensors/" + f"?fields={fields}"
        )

        # Add to the request_url string depending on what optional parameters are
        # passed in. Turn them into a dict of optional parameters
        optional_parameters_dict = {
            "location_type": location_type,
            "read_keys": read_keys,
            "show_only": show_only,
            "modified_since": modified_since,
            "max_age": max_age,
            "nwlng": nwlng,
            "nwlat": nwlat,
            "selng": selng,
            "selat": selat,
        }

        first_optional_parameter_separator = "&"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

    def request_sensor_historic_data(
        self,
        sensor_index,
        fields,
        csv_data_format=False,
        read_key=None,
        privacy=None,
        start_timestamp=None,
        end_timestamp=None,
        average=None,
    ):
        """
        A method to request historic data from a single sensor.

        :param bool csv_data_format: Whether or not the data will be returned in CSV format or JSON format.
                                     True means we use this endpoint https://api.purpleair.com/#api-sensors-get-sensor-history-csv
                                     False means we use this endpoint https://api.purpleair.com/#api-sensors-get-sensor-history
                                      

        ## What's below is straight from the Purpleair api website...

        :param int sensor_index: The sensor_index as found in the JSON for this specific sensor.

        :param (optional) str read_key: This read_key is required for private devices. It is separate to the api_key and each sensor has its own read_key. Submit multiple keys by separating them with a comma (,) character for example: key-one,key-two,key-three.

        :param (optional) str privacy: The privacy of returned data. Sensors can record data while registered as public or private. Obtaining private data requires the sensor's read_key be provided.
                                       `auto` (default if not specified) returns data with privacy matching the sensor's current registration.
                                       `both` returns all data regardless of privacy and adds the private field to the returned data columns.
                                       Allowed values: auto, public, private, both

        :param (optional) int start_timestamp: The time stamp of the first required history entry. Query is executed using data_time_stamp >= start_timestamp. This can be specified as a UNIX time stamp in seconds or an ISO 8601 string.
                                               If not specified, the maximum amount of data for the requested average will be returned up to the provided end_timestamp.
                                               The time_stamp column of data in the response's JSON or CSV will use the same format and/or time zone used in the start_timestamp.

        :param (optional) int end_timestamp: The end time stamp of the history to return. Query is executed using data_time_stamp < end_timestamp. This can be specified as a UNIX time stamp in seconds or an ISO 8601 string.
                                             If not specified, the maximum amount of data for the requested average will be returned starting from the provided start_timestamp.

        :param (optional) int average: The desired average in minutes. One of the following:
                                       0 (real-time), 10 (default if not specified), 30, 60, 360 (6 hour), 1440 (1 day), 10080 (1 week), 43200 (1 month), 525600 (1 year).
                                       The amount of data that can be returned in a single response depends on the average used. Time limits for each average are found in our looping API calls community article.

        :param str fields: The 'Fields' parameter specifies which 'sensor data fields' to include in the response. Not all fields are available as history fields and we will be working to add more as time goes on. Fields marked with an asterisk (*) may not be available when using averages. It is a comma separated list with one or more of the following:

                           Station information and status fields:
                           hardware*, latitude*, longitude*, altitude*, firmware_version*, private, rssi, uptime, pa_latency, memory

                           Environmental fields:
                           humidity, humidity_a, humidity_b, temperature, temperature_a, temperature_b, pressure, pressure_a, pressure_b

                           Miscellaneous fields:
                           voc, voc_a, voc_b, analog_input

                           PM1.0 fields:
                           pm1.0_atm, pm1.0_atm_a, pm1.0_atm_b, pm1.0_cf_1, pm1.0_cf_1_a, pm1.0_cf_1_b

                           PM2.5 fields:
                           pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b

                           PM10.0 fields:
                           pm10.0_atm, pm10.0_atm_a, pm10.0_atm_b, pm10.0_cf_1, pm10.0_cf_1_a, pm10.0_cf_1_b

                           Visibility fields:
                           scattering_coefficient, scattering_coefficient_a, scattering_coefficient_b, deciviews, deciviews_a, deciviews_b, visual_range, visual_range_a, visual_range_b

                           Particle count fields:
                           0.3_um_count, 0.3_um_count_a, 0.3_um_count_b, 0.5_um_count, 0.5_um_count_a, 0.5_um_count_b, 1.0_um_count, 1.0_um_count_a, 1.0_um_count_b, 2.5_um_count, 2.5_um_count_a, 2.5_um_count_b, 5.0_um_count, 5.0_um_count_a, 5.0_um_count_b, 10.0_um_count, 10.0_um_count_a, 10.0_um_count_b

                           For field descriptions, please see the 'sensor data fields'. section.
        """

        history_url_portion = ""
        if csv_data_format:
            history_url_portion = "/history/csv"

        else:
            history_url_portion = "/history"
        
        request_url = (
            self._base_api_v1_request_string
            + "sensors/"
            + f"{sensor_index}"
            + f"{history_url_portion}"
            + f"?fields={fields}"
        )

        # Add to the request_url string depending on what optional parameters are
        # passed in. Turn them into a dict of optional parameters
        optional_parameters_dict = {
            "read_key": read_key,
            "privacy": privacy,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "modified_since": end_timestamp,
            "average": average,
        }

        first_optional_parameter_separator = "&"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

    def request_group_detail_data(self, group_id):
        """
        A method to retrieve a list of all members of a specified group.

        :param int group_id: The group_id of the requested group. This group must be owned by the api_key.
        """

        request_url = self._base_api_v1_request_string + f"groups/{group_id}"
        return send_url_get_request(request_url, self._your_api_read_key)

    def request_group_list_data(self):
        """
        A method to retrieve a list of all groups owned by the provided api_key.
        """

        request_url = self._base_api_v1_request_string + f"groups/"
        return send_url_get_request(request_url, self._your_api_read_key)

    def request_member_data(self, group_id, member_id, fields=None):
        """
        A method to get a members' data from a group to which said member belongs.

        :param int group_id: Groups unique ID.

        :param int member_id: Members unique ID.

        :param (optional) str fields: The 'Fields' parameter specifies which 'sensor data fields' to include in the response. It is a comma separated list with one or more of the following:

            Station information and status fields:
            name, icon, model, hardware, location_type, private, latitude, longitude, altitude, position_rating, led_brightness, firmware_version, firmware_upgrade, rssi, uptime, pa_latency, memory, last_seen, last_modified, date_created, channel_state, channel_flags, channel_flags_manual, channel_flags_auto, confidence, confidence_manual, confidence_auto

            Environmental fields:
            humidity, humidity_a, humidity_b, temperature, temperature_a, temperature_b, pressure, pressure_a, pressure_b

            Miscellaneous fields:
            voc, voc_a, voc_b, ozone1, analog_input

            PM1.0 fields:
            pm1.0, pm1.0_a, pm1.0_b, pm1.0_atm, pm1.0_atm_a, pm1.0_atm_b, pm1.0_cf_1, pm1.0_cf_1_a, pm1.0_cf_1_b

            PM2.5 fields:
            pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5, pm2.5_a, pm2.5_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b

            PM2.5 pseudo (simple running) average fields:
            pm2.5_10minute, pm2.5_10minute_a, pm2.5_10minute_b, pm2.5_30minute, pm2.5_30minute_a, pm2.5_30minute_b, pm2.5_60minute, pm2.5_60minute_a, pm2.5_60minute_b, pm2.5_6hour, pm2.5_6hour_a, pm2.5_6hour_b, pm2.5_24hour, pm2.5_24hour_a, pm2.5_24hour_b, pm2.5_1week, pm2.5_1week_a, pm2.5_1week_b

            PM10.0 fields:
            pm10.0, pm10.0_a, pm10.0_b, pm10.0_atm, pm10.0_atm_a, pm10.0_atm_b, pm10.0_cf_1, pm10.0_cf_1_a, pm10.0_cf_1_b

            Particle count fields:
            0.3_um_count, 0.3_um_count_a, 0.3_um_count_b, 0.5_um_count, 0.5_um_count_a, 0.5_um_count_b, 1.0_um_count, 1.0_um_count_a, 1.0_um_count_b, 2.5_um_count, 2.5_um_count_a, 2.5_um_count_b, 5.0_um_count, 5.0_um_count_a, 5.0_um_count_b, 10.0_um_count 10.0_um_count_a, 10.0_um_count_b

            ThingSpeak fields, used to retrieve data from api.thingspeak.com:
            primary_id_a, primary_key_a, secondary_id_a, secondary_key_a, primary_id_b, primary_key_b, secondary_id_b, secondary_key_b

            For field descriptions, please see the 'sensor data fields'. section.
        """

        request_url = (
            self._base_api_v1_request_string + f"groups/{group_id}/members/{member_id}"
        )

        # Add to the request_url string depending on what optional parameters are
        # passed in. Turn them into a dict of optional parameters
        optional_parameters_dict = {"fields": fields}

        first_optional_parameter_separator = "?"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

    def request_member_historic_data(
        self,
        group_id,
        member_id,
        fields,
        start_timestamp=None,
        end_timestamp=None,
        average=None,
    ):
        """
        A method to get a members' historic data from a group to which said member belongs too.

        :param int group_id: Groups unique ID.

        :param int member_id: Members unique ID.

        :param (optional) int start_timestamp: The time stamp of the first required history entry. Query is executed using data_timestamp >= start_timestamp.
                                    Time can be specified as a UNIX time stamp in seconds or an ISO 8601 string. https://en.wikipedia.org/wiki/ISO_8601.
                                    The time_stamp column in the resulting JSON or CSV will be in the same format and or time zone that you use for this start_timestamp parameter.
                                    If not specified, the last maximum time span for the requested average will be returned.

        :param (optional) int end_timestamp: The end time stamp of the history to return. Query is executed using data_timestamp < end_timestamp.
                                             Time can be specified as a UNIX time stamp in seconds or an ISO 8601 string. https://en.wikipedia.org/wiki/ISO_8601.
                                             If not specified, the maximum time span will be returned starting from the provided start_timestamp.

        :param (optional) int average: The desired average in minutes, one of the following: 0 (real-time), 10 (default if not specified), 30, 60, 360 (6 hour), 1440 (1 day)
                                       Coming soon: 10080 (1 week), 44640 (1 month), 525600 (1 year).

        :param str fields: The 'Fields' parameter specifies which 'sensor data fields' to include in the response. Not all fields are available as history fields and we will be working to add more as time goes on. Fields marked with an asterisk (*) may not be available when using averages. It is a comma separated list with one or more of the following:

                            Station information and status fields:
                            hardware*, latitude*, longitude*, altitude*, firmware_version*, rssi, uptime, pa_latency, memory,

                            Environmental fields:
                            humidity, humidity_a, humidity_b, temperature, temperature_a, temperature_b, pressure, pressure_a, pressure_b

                            Miscellaneous fields:
                            voc, voc_a, voc_b, analog_input

                            PM1.0 fields:
                            pm1.0_atm, pm1.0_atm_a, pm1.0_atm_b, pm1.0_cf_1, pm1.0_cf_1_a, pm1.0_cf_1_b

                            PM2.5 fields:
                            pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b

                            PM10.0 fields:
                            pm10.0_atm, pm10.0_atm_a, pm10.0_atm_b, pm10.0_cf_1, pm10.0_cf_1_a, pm10.0_cf_1_b

                            Visibility fields:
                            scattering_coefficient, scattering_coefficient_a, scattering_coefficient_b, deciviews, deciviews_a, deciviews_b, visual_range, visual_range_a, visual_range_b

                            Particle count fields:
                            0.3_um_count, 0.3_um_count_a, 0.3_um_count_b, 0.5_um_count, 0.5_um_count_a, 0.5_um_count_b, 1.0_um_count, 1.0_um_count_a, 1.0_um_count_b, 2.5_um_count, 2.5_um_count_a, 2.5_um_count_b, 5.0_um_count, 5.0_um_count_a, 5.0_um_count_b, 10.0_um_count, 10.0_um_count_a, 10.0_um_count_b

                            For field descriptions, please see the 'sensor data fields'. section.
        """

        request_url = (
            self._base_api_v1_request_string
            + f"groups/{group_id}/members/{member_id}/history/?fields={fields}"
        )

        # Add to the request_url string depending on what optional parameters are
        # passed in. Turn them into a dict of optional parameters
        optional_parameters_dict = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "average": average,
        }

        first_optional_parameter_separator = "&"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

    def request_members_data(
        self,
        group_id,
        fields,
        location_type=None,
        read_keys=None,
        show_only=None,
        modified_since=None,
        max_age=None,
        nwlng=None,
        nwlat=None,
        selng=None,
        selat=None,
    ):
        """
        A method to get multiple members' data from from a group to which said members belong too.

        :param int group_id: The group_id of the requested group. This group must be owned by the api_key.

        :param str fields: The 'Fields' parameter specifies which 'sensor data fields' to include in the response. It is a comma separated list with one or more of the following:

                            Station information and status fields:
                            name, icon, model, hardware, location_type, private, latitude, longitude, altitude, position_rating, led_brightness, firmware_version, firmware_upgrade, rssi, uptime, pa_latency, memory, last_seen, last_modified, date_created, channel_state, channel_flags, channel_flags_manual, channel_flags_auto, confidence, confidence_manual, confidence_auto

                            Environmental fields:
                            humidity, humidity_a, humidity_b, temperature, temperature_a, temperature_b, pressure, pressure_a, pressure_b

                            Miscellaneous fields:
                            voc, voc_a, voc_b, ozone1, analog_input

                            PM1.0 fields:
                            pm1.0, pm1.0_a, pm1.0_b, pm1.0_atm, pm1.0_atm_a, pm1.0_atm_b, pm1.0_cf_1, pm1.0_cf_1_a, pm1.0_cf_1_b

                            PM2.5 fields:
                            pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5, pm2.5_a, pm2.5_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b

                            PM2.5 pseudo (simple running) average fields:
                            pm2.5_10minute, pm2.5_10minute_a, pm2.5_10minute_b, pm2.5_30minute, pm2.5_30minute_a, pm2.5_30minute_b, pm2.5_60minute, pm2.5_60minute_a, pm2.5_60minute_b, pm2.5_6hour, pm2.5_6hour_a, pm2.5_6hour_b, pm2.5_24hour, pm2.5_24hour_a, pm2.5_24hour_b, pm2.5_1week, pm2.5_1week_a, pm2.5_1week_b

                            PM10.0 fields:
                            pm10.0, pm10.0_a, pm10.0_b, pm10.0_atm, pm10.0_atm_a, pm10.0_atm_b, pm10.0_cf_1, pm10.0_cf_1_a, pm10.0_cf_1_b

                            Visibility fields:
                            scattering_coefficient, scattering_coefficient_a, scattering_coefficient_b, deciviews, deciviews_a, deciviews_b, visual_range, visual_range_a, visual_range_b

                            Particle count fields:
                            0.3_um_count, 0.3_um_count_a, 0.3_um_count_b, 0.5_um_count, 0.5_um_count_a, 0.5_um_count_b, 1.0_um_count, 1.0_um_count_a, 1.0_um_count_b, 2.5_um_count, 2.5_um_count_a, 2.5_um_count_b, 5.0_um_count, 5.0_um_count_a, 5.0_um_count_b, 10.0_um_count 10.0_um_count_a, 10.0_um_count_b

                            ThingSpeak fields, used to retrieve data from api.thingspeak.com:
                            primary_id_a, primary_key_a, secondary_id_a, secondary_key_a, primary_id_b, primary_key_b, secondary_id_b, secondary_key_b

                            For field descriptions, please see the 'sensor data fields'. section.

        :param (optional) int location_type: The location_type of the sensors.
                                             Possible values are: 0 = Outside or 1 = Inside.

        :param (optional) str read_keys: A read_key is required for private devices. It is separate to the api_key and each sensor has its own read_key. Submit multiple keys by separating them with a comma (,) character for example: key-one,key-two,key-three.

        :param (optional) str show_only: A comma (,) separated list of sensor_index values. When provided, the results are limited only to the sensors included in this list.

        :param (optional) int modified_since: The modified_since parameter causes only sensors modified after the provided time stamp to be included in the results. Using the time_stamp value from a previous call (recommended) will limit results to those with new values since the last request. Using a value of 0 will match sensors modified at any time.

        :param (optional) int max_age: Filter results to only include sensors modified or updated within the last number of seconds. Using a value of 0 will match sensors of any age.
                                        Default value: 604800

        :param (optional) int nwlng: A north west longitude for the bounding box.
                                     Use a bounding box to limit the sensors returned to a specific geographic area. The bounding box is defined by two points, a north west latitude/longitude and a south east latitude/longitude.

        :param (optional) int nwlat: A north west latitude for the bounding box.

         :param (optional) int selng: A south east longitude for the bounding box.

         :param (optional) int selat: A south east latitude for the bounding box.

        """

        request_url = (
            self._base_api_v1_request_string
            + f"groups/{group_id}/members?fields={fields}"
        )

        # Add to the request_url string depending on what optional parameters are
        # passed in. Turn them into a dict of optional parameters
        optional_parameters_dict = {
            "location_type": location_type,
            "read_keys": read_keys,
            "show_only": show_only,
            "modified_since": modified_since,
            "max_age": max_age,
            "nwlng": nwlng,
            "nwlat": nwlat,
            "selng": selng,
            "selat": selat,
        }

        first_optional_parameter_separator = "&"
        return send_url_get_request(
            request_url,
            self._your_api_read_key,
            first_optional_parameter_separator,
            optional_parameters_dict,
        )

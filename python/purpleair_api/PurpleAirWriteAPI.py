#!/usr/bin/env python3

"""
Copyright 2024 carlkidcrypto, All rights reserved.
A python3 class designed to send write requests to Purple Air's API.
This class will handle all `write` requests
https://api.purpleair.com/#api-welcome
"""

from purpleair_api.PurpleAirAPIError import PurpleAirAPIError
from purpleair_api.PurpleAirAPIHelpers import (
    debug_log,
    send_url_post_request,
    send_url_delete_request,
)


class PurpleAirWriteAPI:
    """
    The PurpleAirWriteAPI class designed to send valid
    write requests.
    """

    def __init__(self, api_write_key=None):
        """
        :param str api_write_key: A valid PurpleAir API write key.
        """
        # Save off the API key for internal usage
        self._your_api_write_key = api_write_key
        self._base_api_v1_request_string = "https://api.purpleair.com/v1/"

    def post_create_group_data(self, name):
        """
        A method to create a group for sensors.

        :param str name: The name of the group to create.

        :return dict | None: A dictionary containing the created group data.
        """

        post_url = self._base_api_v1_request_string + f"groups"

        return send_url_post_request(post_url, self._your_api_write_key, {"name": name})

    def post_create_member(
        self,
        group_id,
        sensor_index=None,
        sensor_id=None,
        owner_email=None,
        location_type=None,
    ):
        """
        Add a sensor as a member of a group. The group must be owned by the api_key used.
        Supports three parameter combinations:

        - **Option 1** — public sensor by ``sensor_id`` (as printed on the label):
          provide ``group_id`` and ``sensor_id``.
        - **Option 2** — sensor by ``sensor_index`` (from the API):
          provide ``group_id`` and ``sensor_index``.
        - **Option 3** — private sensor by ``sensor_id`` with owner verification:
          provide ``group_id``, ``sensor_id``, ``owner_email``, and optionally ``location_type``.

        :param int group_id: The group_id of the group to add a member to. This group must be owned by the api_key.
        :param int sensor_index: The sensor_index of the new member as found in the JSON for this specific sensor.
        :param str sensor_id: The sensor_id of the new member sensor. This must be AS PRINTED on the sensor's label.
        :param str owner_email: An email address that matches the Owner email as set by previously completing
                                the PurpleAir registration form at www.purpleair.com/register.
        :param int location_type: (optional) The expected location_type of the new member.
                                  Possible values are: 0 = Outside or 1 = Inside.
                                  Required when the target sensor is marked as 'private'.

        :return dict | None: A dictionary containing the created member data.
        :raises PurpleAirAPIError: If an invalid combination of parameters is provided or the API request fails.
        """

        post_url = self._base_api_v1_request_string + f"groups/{group_id}/members"

        if (
            sensor_index is None
            and sensor_id is not None
            and owner_email is None
            and location_type is None
        ):
            # We good, use the sensor id
            debug_log("post_create_member - option 1")
            return send_url_post_request(
                post_url, self._your_api_write_key, {"sensor_id": str(sensor_id)}
            )

        elif (
            sensor_index is not None
            and sensor_id is None
            and owner_email is None
            and location_type is None
        ):
            # We good, use the sensor index
            debug_log("post_create_member - option 2")
            return send_url_post_request(
                post_url, self._your_api_write_key, {"sensor_index": sensor_index}
            )

        elif sensor_index is None and sensor_id is not None and owner_email is not None:
            # We good, use the private sensor id.
            debug_log("post_create_member - option 3")
            return send_url_post_request(
                post_url,
                self._your_api_write_key,
                {
                    "sensor_id": str(sensor_id),
                    "owner_email": owner_email,
                    "location_type": location_type,
                },
            )

        else:
            raise PurpleAirAPIError("Invalid configuration of method parameters!")

    def post_delete_group(self, group_id):
        """
        A method to delete a group for sensors.

        :param int group_id: The group_id of the group to delete

        :return dict | None: A dictionary containing the deletion response.
        """

        post_url = self._base_api_v1_request_string + f"groups/{group_id}"

        return send_url_delete_request(post_url, self._your_api_write_key)

    def post_delete_member(self, group_id, member_id):
        """
        Delete a member from a group.

        :param int group_id: The group_id of the group in which member_id is in.
        :param int member_id: The member_id to delete.

        :return dict | None: A dictionary containing the deletion response.
        """

        post_url = (
            self._base_api_v1_request_string + f"groups/{group_id}/members/{member_id}"
        )

        return send_url_delete_request(post_url, self._your_api_write_key)

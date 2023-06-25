#!/usr/bin/env python3

"""
    Copyright 2023 carlkidcrypto, All rights reserved.
    A python3 class designed to fetch data from Purple Air's new API.
    https://api.purpleair.com/#api-welcome
"""


class PurpleAirAPIError(Exception):
    """
    Custom Exception for our PurpleAirAPI class.
    """

    def __init__(self, message_string):
        self.message = message_string
        super().__init__(self.message)

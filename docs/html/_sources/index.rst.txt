.. PurpleAir API documentation master file, created by
   sphinx-quickstart on Mon Sep 12 21:26:27 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PurpleAirAPI's documentation!
====================================================

PurpleAir API (PAA) is a Python 3 wrapper for the PurpleAir API, providing easy access to air quality sensor data.
This package allows you to interact with PurpleAir sensors through their official API endpoints.

Features
--------

* **Read API**: Query sensor data, get sensor information, and retrieve historical data
* **Write API**: Manage members and sensor configurations (requires write API key)
* **Local API**: Connect directly to local PurpleAir sensors on your network
* **Complete API Coverage**: Access all endpoints provided by the PurpleAir API

Getting Started
---------------

To use the PurpleAir API, you'll need API keys from PurpleAir. You can request them by emailing
contact@purpleair.com with your first and last name.

Installation
~~~~~~~~~~~~

Install via pip::

    python3 -m pip install purple_air_api

Or clone from GitHub::

    git clone https://github.com/carlkidcrypto/purple_air_api.git
    cd purple_air_api
    python3 setup.py install

Quick Example
~~~~~~~~~~~~~

.. code-block:: python

    from purpleair_api.PurpleAirAPI import PurpleAirAPI
    
    # Initialize the API with your keys
    my_paa = PurpleAirAPI(your_api_read_key, your_api_write_key, your_ipv4_address)
    
    # Request sensor data
    sensor_data = my_paa.request_sensor_data(1234)

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   modules

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Additional Resources
====================

* `GitHub Repository <https://github.com/carlkidcrypto/purpleair_api>`_
* `PurpleAir Official API Documentation <https://api.purpleair.com/#api-welcome>`_
* `PyPI Package <https://pypi.org/project/purpleair-api/>`_

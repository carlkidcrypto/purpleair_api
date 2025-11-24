PurpleAirReadAPI module
=======================

Provides read-only access to the PurpleAir API for querying sensor data.
This module does not require write permissions.

Usage Example
-------------

.. code-block:: python

   from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
   
   # Initialize with read key only
   read_api = PurpleAirReadAPI(api_read_key="your_read_key")
   
   # Request single sensor data
   sensor_data = read_api.request_sensor_data(12345)
   
   # Request multiple sensors data
   sensors = read_api.request_multiple_sensors_data("name")

API Reference
-------------

.. automodule:: PurpleAirReadAPI
   :members:
   :undoc-members:
   :show-inheritance:

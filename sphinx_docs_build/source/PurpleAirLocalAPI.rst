PurpleAirLocalAPI module
========================

Provides direct access to PurpleAir sensors on the local network without requiring API keys.
This allows for faster queries and avoids cloud API rate limiting.

Usage Example
-------------

.. code-block:: python

   from purpleair_api.PurpleAirLocalAPI import PurpleAirLocalAPI
   
   # Initialize with local sensor IP addresses
   local_api = PurpleAirLocalAPI(ipv4_address=["192.168.1.100", "192.168.1.101"])
   
   # Request data from local sensor
   sensor_data = local_api.request_local_sensor_data()

API Reference
-------------

.. automodule:: PurpleAirLocalAPI
   :members:
   :undoc-members:
   :show-inheritance:

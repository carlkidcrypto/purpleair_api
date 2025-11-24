PurpleAirAPI module
===================

The main entry point for the PurpleAir API wrapper. This module automatically loads
the appropriate submodules (Read, Write, Local) based on the API keys and configuration
provided during initialization.

Usage Example
-------------

.. code-block:: python

   from purpleair_api.PurpleAirAPI import PurpleAirAPI
   
   # Initialize with all API types
   paa = PurpleAirAPI(
       api_read_key="your_read_key",
       api_write_key="your_write_key",
       ipv4_address=["192.168.1.100"]
   )
   
   # Now you can use read, write, and local methods
   sensor_data = paa.request_sensor_data(12345)

API Reference
-------------

.. automodule:: PurpleAirAPI
   :members:
   :undoc-members:
   :show-inheritance:

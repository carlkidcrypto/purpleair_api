PurpleAirWriteAPI module
========================

Provides write access to the PurpleAir API for managing sensors, members, and configurations.
Requires a write API key with appropriate permissions.

Usage Example
-------------

.. code-block:: python

   from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI
   
   # Initialize with write key
   write_api = PurpleAirWriteAPI(api_write_key="your_write_key")
   
   # Create a new member
   result = write_api.post_create_member(sensor_index=12345)

API Reference
-------------

.. automodule:: PurpleAirWriteAPI
   :members:
   :undoc-members:
   :show-inheritance:

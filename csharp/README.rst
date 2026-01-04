PurpleAir API - C# Bindings
============================

C# bindings for the PurpleAir API using the native C++ library via SWIG.

Prerequisites
-------------

- SWIG 4.x or later
- g++ with C++17 support
- libcurl development headers
- .NET 6.0 SDK or later

Building
--------

The build process automatically generates SWIG wrapper code on the fly.

Build the native library
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make

This runs SWIG to generate the C# bindings and wrapper code, then compiles
the C++ code into ``libpurpleairapi.so``.

To regenerate SWIG bindings only:

.. code-block:: bash

   make swig

Build the C# project
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   dotnet build

Clean generated files
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make clean

Running Tests
-------------

.. code-block:: bash

   cd tests
   dotnet test

Tests are written using xUnit and migrated from the Python test suite.

Usage
-----

.. code-block:: csharp

   using PurpleAirAPI;

   // Create API instance
   var api = new PurpleAirReadAPI("your_api_read_key");

   // Request sensor data
   string result = api.request_sensor_data(1234);
   Console.WriteLine(result);

   // Request multiple sensors
   string sensors = api.request_multiple_sensors_data("name,latitude,longitude");
   Console.WriteLine(sensors);

Creating NuGet Package
----------------------

.. code-block:: bash

   dotnet pack

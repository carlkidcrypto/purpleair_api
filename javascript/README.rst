PurpleAir API - JavaScript/Node.js Bindings
===========================================

JavaScript bindings for the PurpleAir API using the native C++ library via SWIG.

Prerequisites
-------------

- SWIG 4.x or later
- Node.js 14.x or later
- npm
- g++ with C++17 support (or Xcode on macOS)
- libcurl development headers

Building
--------

The build process automatically generates SWIG wrapper code on the fly.

Install dependencies and build:

.. code-block:: bash

   npm install

This runs SWIG to generate the JavaScript bindings and then compiles the
native addon via node-gyp.

Or manually rebuild:

.. code-block:: bash

   npm run build

To regenerate SWIG bindings only:

.. code-block:: bash

   npm run swig

Clean generated files
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   npm run clean

Running Tests
-------------

.. code-block:: bash

   npm test

Tests are written using Jest and migrated from the Python test suite.

Usage
-----

.. code-block:: javascript

   const { PurpleAirReadAPI, PurpleAirWriteAPI, PurpleAirLocalAPI } = require('purpleair-api');

   // Create API instance
   const api = new PurpleAirReadAPI('your_api_read_key');

   // Request sensor data
   const result = api.request_sensor_data(1234);
   console.log(result);

   // Request multiple sensors
   const sensors = api.request_multiple_sensors_data('name,latitude,longitude');
   console.log(sensors);

Publishing to npm
-----------------

To build and publish this package to npm for others to use:

1. **Prepare the package**

   Ensure ``package.json`` has the correct version, name, and metadata.

2. **Login to npm**

   .. code-block:: bash

      npm login

3. **Build the package**

   .. code-block:: bash

      npm run build

4. **Publish to npm**

   For a public package:

   .. code-block:: bash

      npm publish --access public

   For a scoped package (e.g., @username/purpleair-api):

   .. code-block:: bash

      npm publish --access public

5. **Verify publication**

   Check your package at https://www.npmjs.com/package/purpleair-api

Version Bumping
~~~~~~~~~~~~~~~

To release a new version:

.. code-block:: bash

   # For alpha releases (1.4.0aX)
   npm version prerelease --preid=a

   # For beta releases (1.4.0bX)
   npm version prerelease --preid=b

   # For patch releases (1.4.1)
   npm version patch

   # For minor releases (1.5.0)
   npm version minor

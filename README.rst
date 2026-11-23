purple_air_api (PAA)
====================

This is a wrapper for the PurpleAirAPI (PAA) with a **C++ backend and SWIG bindings** for Python, JavaScript, C#, and Go. Details of the API can be found using this link: https://api.purpleair.com/#api-welcome

To use the PurpleAirAPI (PAA), API keys are required. You can get API keys by sending an email to ``contact@purpleair.com`` with a first and last name to assign them to.

**New in CalSemVer**: The library now uses a high-performance C++ backend with SWIG bindings, providing native performance while maintaining full backward compatibility with existing Python code.

|python_tests| |javascript_tests| |csharp_tests| |go_tests| |black| |sphinx_docs|

|codecov| |sonar_gate| |sonar_security| |sonar_maintainability| |codeql|

|pypi_version| |testpypi_version| |pypi_downloads| |npm_version| |npm_downloads| |pypi_dist| |testpypi_dist|

|license|

.. |python_tests| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/python_test.yml?branch=main&style=flat-square&label=Python%20Tests
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/python_test.yml
   :alt: Python Tests
.. |javascript_tests| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/javascript_test.yml?branch=main&style=flat-square&label=JavaScript%20Tests
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/javascript_test.yml
   :alt: JavaScript Tests
.. |csharp_tests| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/csharp_test.yml?branch=main&style=flat-square&label=C%23%20Tests
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/csharp_test.yml
   :alt: C# Tests
.. |go_tests| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/go_test.yml?branch=main&style=flat-square&label=Go%20Tests
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/go_test.yml
   :alt: Go Tests
.. |black| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/python_black.yml?branch=main&style=flat-square&label=Black
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/python_black.yml
   :alt: Black
.. |sphinx_docs| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/python_sphinx_build.yml?branch=main&style=flat-square&label=Sphinx%20Docs
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/python_sphinx_build.yml
   :alt: Sphinx Docs
.. |codecov| image:: https://img.shields.io/codecov/c/github/carlkidcrypto/purpleair_api/main?style=flat-square&label=Codecov
   :target: https://codecov.io/gh/carlkidcrypto/purpleair_api
   :alt: Codecov
.. |sonar_gate| image:: https://sonarcloud.io/api/project_badges/measure?project=carlkidcrypto_purpleair_api&metric=alert_status
   :target: https://sonarcloud.io/summary/new_code?id=carlkidcrypto_purpleair_api
   :alt: SonarCloud Quality Gate
.. |sonar_security| image:: https://sonarcloud.io/api/project_badges/measure?project=carlkidcrypto_purpleair_api&metric=security_rating
   :target: https://sonarcloud.io/summary/new_code?id=carlkidcrypto_purpleair_api
   :alt: SonarCloud Security Rating
.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=carlkidcrypto_purpleair_api&metric=sqale_rating
   :target: https://sonarcloud.io/summary/new_code?id=carlkidcrypto_purpleair_api
   :alt: SonarCloud Maintainability Rating
.. |codeql| image:: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/github-code-scanning/codeql/badge.svg
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/github-code-scanning/codeql
   :alt: CodeQL
.. |pypi_version| image:: https://img.shields.io/pypi/v/purpleair_api?style=flat-square
   :target: https://pypi.org/project/purpleair_api/
   :alt: PyPI Version
.. |testpypi_version| image:: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fpurpleair-api%2Fjson&query=%24.info.version&label=TestPyPI&style=flat-square&color=blue
   :target: https://test.pypi.org/project/purpleair-api/
   :alt: TestPyPI Version
.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/purpleair_api?style=flat-square
   :target: https://pypi.org/project/purpleair_api/
   :alt: PyPI Downloads
.. |npm_version| image:: https://img.shields.io/npm/v/purpleair-api?style=flat-square
   :target: https://www.npmjs.com/package/purpleair-api
   :alt: npm Version
.. |npm_downloads| image:: https://img.shields.io/npm/dm/purpleair-api?style=flat-square
   :target: https://www.npmjs.com/package/purpleair-api
   :alt: npm Downloads
.. |pypi_dist| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/build_and_publish_to_pypi.yml?style=flat-square&label=PyPI%20Distributions
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml
   :alt: PyPI Distributions
.. |testpypi_dist| image:: https://img.shields.io/github/actions/workflow/status/carlkidcrypto/purpleair_api/build_and_publish_to_test_pypi.yml?branch=main&style=flat-square&label=TestPyPI%20Distributions
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml
   :alt: TestPyPI Distributions
.. |license| image:: https://img.shields.io/github/license/carlkidcrypto/purpleair_api?style=flat-square
   :target: https://github.com/carlkidcrypto/purpleair_api/blob/main/LICENSE
   :alt: License

How to Support This Project
----------------------------

.. image:: https://cdn.buymeacoffee.com/buttons/default-orange.png
   :target: https://www.buymeacoffee.com/carlkidcrypto
   :alt: Buy Me A Coffee
   :height: 41
   :width: 174

Purpose
-------

This package is designed to be used for making tools around the PurpleAir API.

For example, PAA data loggers - https://github.com/carlkidcrypto/purpleair_data_logger

Requirements
------------

* Python 3.10 or higher (supports Python 3.10, 3.11, 3.12, 3.13, and 3.14)
* requests library

Installation
------------

Prerequisites
~~~~~~~~~~~~~

The C++ backend requires:

- **Linux/Ubuntu**: ``sudo apt-get install build-essential libcurl4-openssl-dev swig meson ninja-build``
- **macOS**: ``brew install curl swig meson ninja``
- **Windows**: Visual Studio C++, SWIG, curl library, Meson, and Ninja

Installation via pip
~~~~~~~~~~~~~~~~~~~~

You can install the PurpleAir API via pip:

.. code-block:: bash

   python3 -m pip install purpleair_api

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

You can also install PurpleAir API by cloning down this repo:

.. code-block:: bash

   git clone https://github.com/carlkidcrypto/purpleair_api.git
   cd purpleair_api

Multi-Language Support
~~~~~~~~~~~~~~~~~~~~~~

The repository is structured to support multiple languages:

- **Python**: ``cd python && python -m pip install .``
- **JavaScript/Node.js**, **C#**, and **Go** use Meson/Ninja to build the
  native parts first:

  .. code-block:: bash

     meson setup builddir && ninja -C builddir

  Then follow the language-specific steps in each binding's README:

  - `javascript/README.rst <javascript/README.rst>`_
  - `csharp/README.rst <csharp/README.rst>`_
  - `go/README.rst <go/README.rst>`_

- **Native C++**: See `swig/README.rst <swig/README.rst>`_

PurpleAirAPI Usage Example
---------------------------

First we need to import the PurpleAir API (PAA):

.. code-block:: python

   from purpleair_api.PurpleAirAPI import PurpleAirAPI

Next we need to make an instance of PAA:

.. code-block:: python

   my_paa = PurpleAirAPI(your_api_read_key, your_api_write_key, [your_ipv4_address])

Now you can use that PAA instance to do things like:

.. code-block:: python

   retval = my_paa.request_sensor_data(1234)

.. note::
   PurpleAirAPI is the main entry point. It will load read, write, and local submodules
   based on the parameters that are passed in upon construction. If you wish to only use a
   small piece of PurpleAirAPI then see the examples below.

PurpleAirReadAPI Usage Example
-------------------------------

First we need to import the PurpleAirReadAPI:

.. code-block:: python

   from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI

Now we need to make an instance of it:

.. code-block:: python

   my_paa = PurpleAirReadAPI(api_read_key)

Now we can use that instance to do things like:

.. code-block:: python

   retval = my_paa.request_multiple_sensors_data("name")

PurpleAirWriteAPI Usage Example
--------------------------------

First we need to import the PurpleAirWriteAPI:

.. code-block:: python

   from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI

Now we need to make an instance of it:

.. code-block:: python

   my_paa = PurpleAirWriteAPI(api_write_key)

Now we can use that instance to do things like:

.. code-block:: python

   retval = my_paa.post_create_member(group_id=1234, sensor_index=5678)

PurpleAirLocalAPI Usage Example
--------------------------------

First we need to import the PurpleAirLocalAPI:

.. code-block:: python

   from purpleair_api.PurpleAirLocalAPI import PurpleAirLocalAPI

Now we need to make an instance of it:

.. code-block:: python

   my_paa = PurpleAirLocalAPI(["ipv4_address"])

Now we can use that instance to do things like:

.. code-block:: python

   retval = my_paa.request_local_sensor_data()

Tests
-----

Refer to the test `README <python/tests/README.rst>`_

Documentation
-------------

Full API documentation is available at https://carlkidcrypto.github.io/purpleair_api/

----

*This content was generated by AI and reviewed by humans. Mistakes may still occur. PRs for corrections are welcome.*

Matter Device Converter (Matter 1.5.1)
--------------------------------------
Map PurpleAir sensor data to **Matter** device type structures for use with
Matter-compatible ecosystems (Apple Home, Google Home, Alexa, SmartThings,
Home Assistant Matter integration).

Supports Matter 1.5.1 Air Quality Sensor (Device Type 0x002D), Temperature Sensor,
and Environmental Sensor device types with full EPA AQI calculation.

.. code-block:: python

   from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
   from purpleair_api.PurpleAirMatterConverter import PurpleAirMatterConverter

   pa = PurpleAirReadAPI("YOUR_READ_API_KEY")
   raw = pa.request_sensor_data(282168)

   matter_device = PurpleAirMatterConverter.to_air_quality_sensor(raw)
   print(matter_device["air_quality_summary"])
   # {'epa_aqi': 68, 'epa_category': 'Moderate',
   #  'matter_air_quality_rating': 'GOOD', ...}

See the Matter implementation guide at ``sphinx_docs_build/source/matter_implementation.rst`` or
``docs/html/matter_implementation.html`` after building, or read the rendered guide online at
https://carlkidcrypto.github.io/purpleair_api/matter_implementation.html. The API reference
remains available at ``sphinx_docs_build/source/PurpleAirMatterConverter.rst``.

References:

- Matter 1.5.1 Core Specification (CSA, 2024) — https://csa-iot.org/developer-resource/specifications/
- Air Quality Measurement Cluster (0x005D) — https://github.com/project-chip/matter
- EPA AQI Calculation — https://www.airnow.gov/sites/default/files/2022-05/AQI-Basics-Calculation.pdf

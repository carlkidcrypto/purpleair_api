purple_air_api (PAA)
====================

This is a python3 wrapper for the new PurpleAirAPI (PAA) with a **C++ backend and SWIG bindings** for Python3, JavaScript, and C#. Details of the API can be found using this link: https://api.purpleair.com/#api-welcome

To use the PurpleAirAPI (PAA) api keys are required. You can get API keys by sending an email to ``contact@purpleair.com`` with a first and last name to assign them to.

**New in v2.0**: The library now uses a high-performance C++ backend with SWIG bindings, providing native performance while maintaining full backward compatibility with existing Python code.

.. image:: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml/badge.svg
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml
   :alt: PyPI Distributions

.. image:: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml/badge.svg
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml
   :alt: TestPyPI Distributions

.. image:: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/black.yml/badge.svg
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/black.yml
   :alt: Black

.. image:: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/tests.yml/badge.svg?branch=main
   :target: https://github.com/carlkidcrypto/purpleair_api/actions/workflows/tests.yml
   :alt: Tests

.. image:: https://img.shields.io/github/downloads/carlkidcrypto/purpleair_api/total.svg?style=flat-square&label=all%20downloads
   :target: https://github.com/carlkidcrypto/purpleair_api/releases
   :alt: Total download count

.. image:: https://img.shields.io/github/downloads/carlkidcrypto/purpleair_api/v1.3.1/total.svg?style=flat-square
   :target: https://github.com/carlkidcrypto/purpleair_api/releases/tag/v1.3.1
   :alt: Latest release download count

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

Installation
------------

Prerequisites
~~~~~~~~~~~~~

The C++ backend requires:

- **Linux/Ubuntu**: ``sudo apt-get install build-essential libcurl4-openssl-dev swig``
- **macOS**: ``brew install curl swig``
- **Windows**: Visual Studio C++, SWIG, and curl library

Installation via pip
~~~~~~~~~~~~~~~~~~~~

You can install the PurpleAir API via pip:

.. code-block:: bash

   python3 -m pip install purple_air_api

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

You can also install PurpleAir API by cloning down this repo:

.. code-block:: bash

   git clone https://github.com/carlkidcrypto/purple_air_api.git
   cd purple_air_api
   python3 setup.py install

For detailed build instructions for C++, JavaScript, and C# bindings, see `BUILD_CPP.md <BUILD_CPP.md>`_.

PurpleAirAPI Usage Example
---------------------------

First we need to import the PurpleAir API (PAA):

.. code-block:: python

   from purpleair_api.PurpleAirAPI import PurpleAirAPI

Next we need to make an instance of PAA:

.. code-block:: python

   my_paa = PurpleAirAPI(your_api_read_key, your_api_write_key, your_ipv4_address)

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

   retval = my_paa.post_create_member(1234)

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

Refer to the test `README <tests/README.rst>`_

Documentation
-------------

Full API documentation is available at https://carlkidcrypto.github.io/purpleair_api/

----

*This content was generated by AI and reviewed by humans. Mistakes may still occur. PRs for corrections are welcome.*

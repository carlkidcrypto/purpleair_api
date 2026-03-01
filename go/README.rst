PurpleAir API - Go Bindings
============================

Go bindings for the PurpleAir API, using SWIG and C++ backend.

Requirements
------------

- Go 1.21 or later
- SWIG 4.0 or later
- libcurl development headers
- C++17 compatible compiler (g++ or clang++)

Building
--------

.. code-block:: bash

   # Generate SWIG wrappers and build static library
   cd go
   make all

   # Build and test
   make test

   # Clean
   make clean

Usage
-----

After building, import the package in your Go code:

.. code-block:: go

   package main

   import (
       "fmt"
       purpleairapi "github.com/carlkidcrypto/purpleair_api/go/purpleairapi"
   )

   func main() {
       api := purpleairapi.NewPurpleAirReadAPI("your-read-key")
       data := api.Request_sensor_data(12345, "", "")
       fmt.Println(data)
   }

Notes
-----

- The base implementation is in C++ (``swig/``).
- SWIG generates the Go bindings from the C++ headers.
- CGO is required to compile this package.
- libcurl must be installed on the target system.

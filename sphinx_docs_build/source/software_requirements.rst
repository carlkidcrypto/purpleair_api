Software Requirements
=====================

This document defines the software requirements for the PurpleAir API (``purpleair_api``) package.
Each requirement is identified by a unique feature-grouped ID in the format ``[PREFIX-nn]``,
where the prefix indicates the feature area:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Prefix
     - Feature Area
   * - ``GEN``
     - General package & platform requirements
   * - ``CLIENT``
     - Unified PurpleAirAPI client class
   * - ``READ``
     - Cloud Read API operations
   * - ``WRITE``
     - Cloud Write API operations
   * - ``LOCAL``
     - Local network sensor operations
   * - ``MATTER``
     - Matter standard device & cluster conversion
   * - ``BIND``
     - Unified C++ Core and SWIG Multi-Language Bindings
   * - ``BUILD``
     - Meson Unified Build System & WrapDB Dependencies
   * - ``PKG``
     - Multi-Language Packaging and Distribution
   * - ``ERR``
     - Error handling and exception hierarchy
   * - ``HELP``
     - Request helpers and utility functions
   * - ``TEST``
     - Testing and code coverage
   * - ``QUAL``
     - Code quality, formatting, and linting
   * - ``DOCS``
     - Documentation and landing page
   * - ``CICD``
     - CI/CD pipelines, concurrency, and release automation

Functional Requirements
-----------------------

General Requirements
~~~~~~~~~~~~~~~~~~~~

[GEN-01] The system shall provide a unified multi-language library centered around a C++17 core
with SWIG bindings for Python, JavaScript/Node.js, C#, Go, and Java, alongside a high-level Python
package installable via ``pip`` for interacting with PurpleAir air quality sensors via cloud and
local network APIs.

[GEN-02] The system shall support the following runtime environments and platforms:

* Python 3.10, 3.11, 3.12, 3.13, and 3.14 across Linux, macOS, and Windows.
* Node.js LTS versions 18.x, 20.x, 22.x, and 24.x across Linux, macOS, and Windows.
* C# / .NET 6.0 and 8.0 across Linux, macOS, and Windows.
* Go 1.21, 1.22, and 1.23 across Linux and macOS.
* Java OpenJDK 17 and 21 across Linux and macOS.

[GEN-03] The Python system shall use the ``requests`` library for executing HTTP and HTTPS requests,
while the native C++ core shall use ``libcurl`` for cross-platform network communication.

[GEN-04] The package initializer (``purpleair_api/__init__.py``) shall remain clean and lightweight
to avoid circular dependencies or unwanted side-effects on import.

Unified Client Class
~~~~~~~~~~~~~~~~~~~~

[CLIENT-01] The system shall provide a unified entry-point class ``PurpleAirAPI`` that inherits from
and combines ``PurpleAirReadAPI``, ``PurpleAirWriteAPI``, and ``PurpleAirLocalAPI``.

[CLIENT-02] The ``PurpleAirAPI`` initializer shall accept ``your_api_read_key``,
``your_api_write_key``, and ``your_ipv4_address`` (list of IPv4 strings) as optional arguments.

[CLIENT-03] The ``PurpleAirAPI`` initializer shall raise ``PurpleAirAPIError`` if none of
``your_api_read_key``, ``your_api_write_key``, or ``your_ipv4_address`` are provided.

[CLIENT-04] When a read key is provided, ``PurpleAirAPI`` shall verify the key against the
``https://api.purpleair.com/v1/keys`` endpoint and verify that the key type is ``READ``;
otherwise, it shall raise ``PurpleAirAPIError``.

[CLIENT-05] When a write key is provided, ``PurpleAirAPI`` shall verify the key against the
``https://api.purpleair.com/v1/keys`` endpoint and verify that the key type is ``WRITE``;
otherwise, it shall raise ``PurpleAirAPIError``.

[CLIENT-06] The ``PurpleAirAPI`` class shall expose properties ``get_api_versions``,
``get_api_key_last_checked``, and ``get_api_key_type`` providing metadata about verified keys.

[CLIENT-07] Debug logging within ``PurpleAirAPI`` shall not log sensitive API keys in plain text.

Cloud Read API Operations
~~~~~~~~~~~~~~~~~~~~~~~~~

[READ-01] The system shall provide a ``PurpleAirReadAPI`` class initialized with an optional
``api_read_key`` parameter.

[READ-02] The system shall implement ``request_sensor_data(sensor_index, read_key, fields)`` to query
data for a single sensor by its index, with optional sensor-specific read key and field filters.

[READ-03] The system shall implement ``request_multiple_sensors_data(fields, location_type, read_keys,
show_only, modified_since, max_age, nwlng, nwlat, selng, selat)`` to retrieve data for multiple
sensors with support for geographic bounding boxes, location types (inside/outside), and timestamp
filters.

[READ-04] The system shall implement ``request_sensor_historic_data(sensor_index, read_key,
fields, start_timestamp, end_timestamp, average)`` to query historical readings with configurable
averaging periods (e.g., 10 minutes, 30 minutes, 1 hour, 6 hours, 1 day, 1 week, 1 month, 1 year).

[READ-05] The system shall implement ``request_group_list_data()`` to retrieve all sensor groups
associated with the authenticated account.

[READ-06] The system shall implement ``request_group_detail_data(group_id)`` to retrieve metadata
and sensor members for a specific group.

[READ-07] The system shall implement ``request_member_data(group_id, member_id, fields)`` to
retrieve current readings for an individual member of a sensor group.

[READ-08] The system shall implement ``request_member_historic_data(group_id, member_id, fields,
start_timestamp, end_timestamp, average)`` to retrieve historical readings for an individual group
member.

[READ-09] The system shall implement ``request_members_data(group_id, fields, location_type,
read_keys, show_only, modified_since, max_age, nwlng, nwlat, selng, selat)`` to query data across
all members of a sensor group.

Cloud Write API Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

[WRITE-01] The system shall provide a ``PurpleAirWriteAPI`` class initialized with an optional
``api_write_key`` parameter.

[WRITE-02] The system shall implement ``post_create_group_data(name)`` to create a new sensor group.

[WRITE-03] The system shall implement ``post_create_group_member_data(group_id, sensor_index,
sensor_id)`` to add a sensor to an existing group.

[WRITE-04] The system shall implement ``delete_group_member(group_id, member_id)`` to remove a sensor
member from a group.

[WRITE-05] The system shall implement ``delete_group(group_id)`` to delete an entire sensor group.

Local Network Sensor Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[LOCAL-01] The system shall provide a ``PurpleAirLocalAPI`` class initialized with an optional
``ipv4_address`` parameter (single IPv4 string or list of IPv4 strings).

[LOCAL-02] The system shall implement ``request_local_sensor_data()`` to query the ``/json`` endpoint
of local sensors directly over the local network via HTTP GET.

[LOCAL-03] When initialized with multiple IP addresses, ``request_local_sensor_data()`` shall return
a dictionary mapping each IP address to its corresponding sensor response dictionary.

[LOCAL-04] When initialized with a single IP address, ``request_local_sensor_data()`` shall return
the sensor response dictionary directly.

[LOCAL-05] If a local sensor is unreachable or returns an HTTP error, the system shall raise
``PurpleAirDeviceError`` or ``PurpleAirDeviceOfflineError`` with context.

Matter Device and Cluster Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[MATTER-01] The system shall provide a ``PurpleAirMatterConverter`` class capable of converting
raw sensor dictionaries (from either cloud or local APIs) into Matter-compliant cluster attributes
and device types.

[MATTER-02] The converter shall support Air Quality cluster (cluster ID ``0x005B``) mapping with
EPA Air Quality Index (AQI) calculation based on PM2.5 readings per 40 CFR Part 58 breakpoints.

[MATTER-03] The converter shall map PM2.5 concentrations to the PM2.5 Concentration Measurement
cluster (cluster ID ``0x042A``) with 1 µg/m³ precision.

[MATTER-04] The converter shall map humidity readings to the Relative Humidity Measurement cluster
(cluster ID ``0x0405``) scaled to Matter 0.01% relative humidity precision.

[MATTER-05] The converter shall map temperature and barometric pressure readings from Fahrenheit to Celsius
(for Matter 0.01 °C precision) and PSI to kPa (for Matter 0.1 kPa precision).

[MATTER-06] The system shall handle offline or unreachable sensors by setting air quality
ratings to ``UNKNOWN`` (``0x00``) and reporting appropriate status flags per Matter specifications.

SWIG Multi-Language Bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[BIND-01] The system shall provide a native C++17 core engine under ``swig/include/`` and ``swig/src/``
implementing PurpleAir Cloud Read, Cloud Write, and Local sensor operations using ``libcurl``.

[BIND-02] SWIG interface definitions under ``swig/interface/`` (``purpleairapi_base.i``, ``purpleairapi_go.i``)
shall generate type-safe wrapper code across Python, JavaScript (Node-API), C#, Go, and Java.

[BIND-03] For JavaScript / Node.js, the SWIG bindings shall target Node-API (``-javascript -napi``)
via ``node-addon-api`` to guarantee native binary compatibility across Node.js LTS versions 18 through 24.

[BIND-04] For C# / .NET, the SWIG bindings shall emit P/Invoke interop code, build shared libraries
without the ``lib`` prefix on Windows (``name_prefix: host_machine.system() == 'windows' ? '' : 'lib'``),
and link with static MinGW runtime arguments (``-static-libgcc``, ``-static-libstdc++``) when compiling
with GCC on Windows.

[BIND-05] For Go, the SWIG bindings shall generate ``cgo``-compatible wrappers and package definitions
under ``go/purpleairapi/`` supporting standard Go toolchains (``go test ./tests/...``).

[BIND-06] For Java, the SWIG bindings shall generate JNI wrappers and Java classes under the
``com.purpleair.api`` package, compiled into a standalone JAR.

Meson Unified Build System
~~~~~~~~~~~~~~~~~~~~~~~~~~

[BUILD-01] The system shall use Meson (>=0.64.0) and Ninja as the centralized build system orchestrating
compilation of the C++ core and language subprojects (``swig/``, ``csharp/``, ``javascript/``, ``go/``,
and ``java/``).

[BUILD-02] The build configuration shall define options (``csharp_bindings``, ``go_bindings``,
``javascript_bindings``, ``enable_java_bindings``) allowing independent enabling or disabling of
language targets.

[BUILD-03] The Meson build system shall provide WrapDB fallback files (``subprojects/curl.wrap``) to
automatically compile and link ``libcurl`` on platforms lacking system-wide ``pkg-config`` installations
(e.g., Windows GitHub Actions runners).

[BUILD-04] The Python package shall use ``meson-python`` as the PEP 517 build backend via ``python/meson.build``
and ``python/pyproject.toml`` for building native extension wheels and source distributions.

Multi-Language Packaging and Distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[PKG-01] Python packages (source distributions and binary wheels) shall be built using ``meson-python``
and distributed to PyPI and TestPyPI.

[PKG-02] JavaScript packages shall compile native Node-API addons via ``node-gyp`` with ``binding.gyp``
and be packaged and published to npm as ``purpleair_api``.

[PKG-03] C# packages shall be compiled with ``dotnet pack`` producing signed NuGet packages
(``PurpleAirAPI.nupkg``) bundling native runtimes across ``win-x64``, ``linux-x64``, and ``osx-x64``.

Error and Exception Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[ERR-01] The system shall provide a base exception class ``PurpleAirAPIError`` inheriting from
Python's standard ``Exception``.

[ERR-02] The system shall provide ``PurpleAirDeviceError`` and ``PurpleAirDeviceOfflineError``
for local device connectivity and communication failures.

[ERR-03] HTTP response errors shall capture and surface the HTTP status code, URL, and response
body from the PurpleAir API service in error messages.

Helper and Utility Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[HELP-01] The system shall provide ``PurpleAirAPIHelpers`` containing reusable URL construction,
parameter formatting, and HTTP request dispatching methods (``send_url_get_request``,
``send_url_post_request``, ``send_url_delete_request``).

[HELP-02] Common API query parameters (such as lists of fields or read keys) shall be automatically
comma-separated and properly URL-encoded.

[HELP-03] The system shall support a debug mode toggled via ``debug_log`` without leaking sensitive
credentials in logs.

Non-Functional Requirements
---------------------------

Testing and Code Coverage
~~~~~~~~~~~~~~~~~~~~~~~~~

[TEST-01] The Python package shall maintain 100% statement and branch code coverage across all modules
in ``python/purpleair_api``.

[TEST-02] All Python unit tests, test configuration, and requirements shall reside under ``python/tests/``,
with code coverage measured via ``python/tests/.coveragerc``.

[TEST-03] Each language binding shall maintain its own dedicated test suite under ``<language>/tests/``
(e.g., ``python/tests/``, ``csharp/tests/``, ``javascript/tests/``, ``go/tests/``, and ``java/tests/``).

[TEST-04] Unit tests shall simulate HTTP responses (e.g. via ``requests_mock`` in Python or mock handlers
in other languages) without requiring live network access during test runs.

[TEST-05] Automated CI matrix workflows shall execute test suites across Linux, macOS, and Windows runners
for all supported runtimes.

Code Quality and Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[QUAL-01] All Python code shall adhere to the Black code style and pass automated formatting checks in CI.

[QUAL-02] All JavaScript, TypeScript, and JSON files shall adhere to Prettier formatting standards.

[QUAL-03] All C# code shall adhere to CSharpier formatting standards.

[QUAL-04] All GitHub Actions workflow YAML files shall adhere to strict formatting and pass validation via
``yamllint`` using the repository's ``.yamllint`` configuration.

[QUAL-05] Workflows managed by GitHub Agentic Workflows (``gh-aw``) shall compile cleanly without warnings
or errors via ``gh aw compile``.

[QUAL-06] The codebase shall pass SonarQube Cloud Quality Gate standards on new code (zero bugs, zero
vulnerabilities, security rating A, and new code duplication <= 3%).

[QUAL-07] Documentation directories (``docs/**``, ``sphinx_docs_build/**``) and language test directories
(``*/tests/**``) shall be excluded from SonarQube copy-paste detection via root ``.sonarcloud.properties``.

Documentation
~~~~~~~~~~~~~

[DOCS-01] Project documentation shall be authored in reStructuredText (reST) and built using
Sphinx with the Furo theme.

[DOCS-02] All public modules, classes, and methods shall have comprehensive docstrings compliant
with Sphinx ``autodoc`` standards.

[DOCS-03] The project shall maintain a dedicated landing page under ``sphinx_docs_build/landing``
that compiles a version switcher linking to the latest documentation and all historical releases.

[DOCS-04] The root documentation directory ``docs/`` shall contain a ``.nojekyll`` file to prevent
GitHub Pages from ignoring directories with leading underscores (such as ``_static/`` and ``_sources/``).

[DOCS-05] Sphinx documentation builds in CI shall enforce ``SPHINXOPTS="-W"`` to treat all warnings
as errors, ensuring that broken cross-references or invalid reST markup fail the build.

CI/CD and Automation
~~~~~~~~~~~~~~~~~~~~

[CICD-01] All CI workflows shall enforce concurrency groups named after their respective workflow
file (e.g., ``group: sphinx_build``) with ``cancel-in-progress: true`` enabled.

[CICD-02] Fresh pushes to open pull requests shall immediately cancel previous in-progress runs
for that workflow and start a new run on the latest commit.

[CICD-03] Pushes to the ``main`` branch shall cancel previous runs for that workflow and execute
against the latest commit on ``main``.

[CICD-04] On every commit pushed to ``main``, the documentation workflow shall build both the latest
documentation and the landing page, and deploy the updated site to GitHub Pages via
``actions/deploy-pages@v5``.

[CICD-05] When a new release is published (``on: release: types: [published]``), the documentation
workflow shall:

* Check out the repository at the release tag.
* Build versioned documentation into ``docs/html_${VERSION}/``.
* Switch to ``main`` and copy the versioned directory into ``docs/``.
* Update the version list sentinels (``.. VERSION_LIST_START`` / ``.. VERSION_LIST_END``) in
  ``sphinx_docs_build/landing/source/index.rst``.
* Rebuild the landing page.
* Automatically create a pull request into ``main`` with the versioned docs and updated index using
  ``peter-evans/create-pull-request@v8``.

[CICD-06] Distribution packaging for TestPyPI and PyPI shall be extracted into reusable composite
GitHub Actions, invoking ``pypa/gh-action-pypi-publish`` directly at the job step level for OIDC
Trusted Publishing compatibility.

[CICD-07] Windows runner workflow execution shall isolate PowerShell (``pwsh``) steps from bash path
mangling when running native builds or passing workspace directory paths.

[CICD-08] Multi-language publishing workflows (PyPI, npm, NuGet) shall execute exclusively on release
events or authorized manual triggers, with branch guards strictly prohibiting publishing from non-main
branches.

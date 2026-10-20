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

[GEN-01] The system shall provide a pure Python package installable via ``pip`` for interacting
with PurpleAir air quality sensors via cloud and local network APIs.

[GEN-02] The system shall support Python 3.10, 3.11, 3.12, 3.13, and 3.14 across Linux, macOS,
and Windows operating systems.

[GEN-03] The system shall use the ``requests`` library for executing HTTP and HTTPS requests.

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

[READ-10] The system shall implement ``request_organization_data()`` to query organization-level
sensor allocations and metadata.

Cloud Write API Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

[WRITE-01] The system shall provide a ``PurpleAirWriteAPI`` class initialized with an optional
``api_write_key`` parameter.

[WRITE-02] The system shall implement ``post_create_group_data(name)`` to create a new sensor group
on the PurpleAir cloud service.

[WRITE-03] The system shall implement ``post_create_member(group_id, sensor_index, sensor_id)`` to
add a sensor member to a designated group using its sensor index or sensor ID.

[WRITE-04] The system shall implement ``post_delete_group(group_id)`` to delete an existing sensor
group.

[WRITE-05] The system shall implement ``post_delete_member(group_id, member_id)`` to remove a member
from a sensor group.

Local Network Sensor Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[LOCAL-01] The system shall provide a ``PurpleAirLocalAPI`` class initialized with a list of IPv4
address strings representing local network sensors.

[LOCAL-02] The ``PurpleAirLocalAPI`` initializer shall validate IPv4 address formatting and raise
``PurpleAirAPIError`` if the address list is empty, non-list, or contains invalid IP strings.

[LOCAL-03] The system shall implement ``request_local_sensor_data()`` to query sensor data directly
over HTTP from each configured sensor at ``http://<ipv4>/json``.

[LOCAL-04] The system shall raise ``PurpleAirDeviceOfflineError`` with clear diagnostic details
when a local sensor is unreachable or encounters a network error.

Matter Standards Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~

[MATTER-01] The system shall provide a ``PurpleAirMatterConverter`` class compliant with the
Connectivity Standards Alliance (CSA) Matter 1.5.1 Specification.

[MATTER-02] The system shall convert PurpleAir sensor data into Matter Air Quality Sensor Device
Type structures (Device Type ID ``0x002D``).

[MATTER-03] The system shall map readings into standard Matter clusters:

* Air Quality Measurement Cluster (``0x005D``)
* Temperature Measurement Cluster (``0x0402``)
* Relative Humidity Measurement Cluster (``0x0405``)
* Barometric Pressure Measurement Cluster (``0x0403``)
* Carbon Dioxide Concentration Measurement Cluster (``0x040D``)

[MATTER-04] The system shall calculate EPA Air Quality Index (AQI) values and ratings from PM2.5
measurements per official EPA AQI piecewise linear breakpoint equations.

[MATTER-05] The system shall provide unit conversion utilities including Fahrenheit to Celsius
(for Matter 0.01 °C precision) and PSI to kPa (for Matter 0.1 kPa precision).

[MATTER-06] The system shall handle offline or unreachable sensors by setting air quality
ratings to ``UNKNOWN`` (``0x00``) and reporting appropriate status flags per Matter specifications.

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

[TEST-01] The system shall maintain 100% statement and branch code coverage across all modules
in the package.

[TEST-02] Unit tests shall run via Python's standard ``unittest`` test runner with ``coverage.py``.

[TEST-03] Unit tests shall use ``requests_mock`` to simulate HTTP responses for all cloud and local
endpoints without making live network calls during test execution.

[TEST-04] Unit tests shall execute cleanly across Ubuntu, macOS, and Windows runners for all
supported Python versions (3.10 through 3.14).

Code Quality and Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[QUAL-01] All Python code shall adhere to the Black code style and pass automated formatting
checks in CI (``.github/workflows/black.yml``).

[QUAL-02] All GitHub Actions workflow YAML files shall adhere to strict formatting and pass
validation via ``yamllint`` using the repository's ``.yamllint`` configuration.

[QUAL-03] Workflows managed by GitHub Agentic Workflows (``gh-aw``) shall compile cleanly
without warnings or errors via ``gh aw compile``.

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

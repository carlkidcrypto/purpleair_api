PurpleAirMatterConverter module
===============================

.. contents::
   :local:
   :depth: 2

Overview
--------

The ``purpleair_api.PurpleAirMatterConverter`` module maps PurpleAir sensor readings to
Matter-compatible device type structures per the **Matter 1.5.1 Core
Specification** (Connectivity Standards Alliance, 2024).

This enables PurpleAir sensors to be exposed through any Matter-compatible
bridge — including Apple Home, Google Home, Amazon Alexa, Samsung SmartThings,
and Home Assistant — by providing data in the canonical format those platforms
consume.

.. note::

   This module generates *Matter device data structures*. It does **not**
   implement the full Matter protocol stack. A Matter bridge (e.g.
   ``python-matter-server`` or the Home Assistant Matter integration) is
   required to actually commission and serve these devices on a Matter network.

References
----------

-  `Matter 1.5.1 Core Specification <https://csa-iot.org/developer-resource/specifications/>`_
   — Connectivity Standards Alliance, 2024.
-  `Matter Air Quality Sensor Device Type
   <https://github.com/project-chip/matter.js/blob/main/docs/API.md>`_
   — Section 11.3, Matter Device Library.
-  `Air Quality Measurement Cluster (0x005D) <https://github.com/project-chip/matter/tree/main/src/matter/clusters/AirQualityMeasurementCluster>`_
   — Matter.js implementation reference.
-  `Temperature Measurement Cluster (0x0402)
   <https://github.com/project-chip/matter/tree/main/src/matter/clusters/TemperatureMeasurementCluster>`_
   — Matter.js implementation reference.
-  `Relative Humidity Measurement Cluster (0x0405)
   <https://github.com/project-chip/matter/tree/main/src/matter/clusters/HumidityMeasurementCluster>`_
   — Matter.js implementation reference.
-  `Barometric Pressure Measurement Cluster (0x0403)
   <https://github.com/project-chip/matter/tree/main/src/matter/clusters/PressureMeasurementCluster>`_
   — Matter.js implementation reference.
-  `EPA AQI Technical Assistance Document (2012 revision)
   <https://www.airnow.gov/sites/default/files/2022-05/AQI-Basics-Calculation.pdf>`_
   — AQI breakpoint table and formula.
-  `python-matter-server
   <https://github.com/home-assistant-libs/python-matter-server>`_
   — Reference Python Matter bridge server.

Installation
------------

``PurpleAirMatterConverter`` is included with the ``purpleair_api`` package.
No additional dependencies are required beyond ``requests``.

.. code-block:: bash

   pip install purpleair_api

Quick Start
-----------

.. code-block:: python

   from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
   from purpleair_api.PurpleAirMatterConverter import PurpleAirMatterConverter

   # Fetch sensor data from PurpleAir
   pa = PurpleAirReadAPI("YOUR_PURPLEAIR_READ_API_KEY")
   raw = pa.request_sensor_data(282168)

   # Convert to Matter Air Quality Sensor structure
   matter_device = PurpleAirMatterConverter.to_air_quality_sensor(raw)

   print(matter_device["device_type"])      # {'id': 45, 'label': 'Air Quality Sensor', ...}
   print(matter_device["air_quality_summary"])  # {'epa_aqi': 68, 'epa_category': 'Moderate', ...}

Field Mapping
-------------

The following table shows how PurpleAir API fields map to Matter clusters
and attributes.

.. list-table::
   :header-rows: 1
   :widths: 30 30 20 20

   *  - PurpleAir Field
      - Matter Cluster
      - Matter Attribute
      - Unit

   *  - ``pm2.5``
      - Air Quality Measurement (0x005D)
      - ``measuredValue`` (scaled ×100)
      - µg/m³

   *  - ``pm1.0``
      - Air Quality Measurement (0x005D)
      - ``pm1Density`` (scaled ×100)
      - µg/m³

   *  - ``pm10.0``
      - Air Quality Measurement (0x005D)
      - ``pm10Density`` (scaled ×100)
      - µg/m³

   *  - ``voc``
      - Air Quality Measurement (0x005D)
      - ``vocDensity`` (scaled ×100)
      - µg/m³

   *  - *(computed)*
      - Air Quality Measurement (0x005D)
      - ``airQuality`` enum
      - category

   *  - *(computed)*
      - Air Quality Measurement (0x005D)
      - ``aqiRating`` enum
      - rating

   *  - ``temperature`` (°F)
      - Temperature Measurement (0x0402)
      - ``measuredValue`` (scaled ×100)
      - °C

   *  - ``humidity``
      - Relative Humidity Measurement (0x0405)
      - ``measuredValue`` (scaled ×100)
      - %

   *  - ``pressure`` (PSI)
      - Barometric Pressure Measurement (0x0403)
      - ``measuredValue`` (scaled ×10)
      - kPa

Matter Scaled-Integer Convention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matter clusters store numeric values as **scaled integers** to avoid
floating-point complexity in the protocol:

-  Temperature: ``round(celsius × 100)`` — e.g., 23.45 °C → **2345**
-  Humidity:    ``round(percent  × 100)`` — e.g., 45.6 %  → **4560**
-  Pressure:    ``round(kPa     × 10)``  — e.g., 101.3 kPa → **1013**
-  PM densities: ``round(ug_m3  × 100)`` — e.g., 12.3 µg/m³ → **1230**

The ``_raw`` fields in the output dictionary retain the original floating-point
values for debugging and display purposes.

EPA AQI Computation
~~~~~~~~~~~~~~~~~~~

PurpleAir provides raw PM2.5 readings but not the EPA Air Quality Index.
:class:`EpaAqiCalculator` applies the EPA's piecewise-linear formula:

.. code-block:: text

   AQI = ((I_high - I_low) / (C_high - C_low)) × (C - C_low) + I_low

Where:

- **C** = PM2.5 24-hour average concentration (µg/m³)
- **C_low, C_high** = concentration breakpoints from the EPA table
- **I_low, I_high** = AQI breakpoints corresponding to ``C_low, C_high``

Matter Air Quality Rating is then derived from the computed AQI:

.. list-table::
   :header-rows: 1

   *  - AQI Range
      - EPA Category
      - Matter ``airQuality`` Value

   *  - 0–50
      - Good
      - 1 (Excellent)

   *  - 51–100
      - Moderate
      - 2 (Good)

   *  - 101–150
      - Unhealthy for Sensitive Groups
      - 3 (Fair)

   *  - 151–200
      - Unhealthy
      - 4 (Poor)

   *  - 201–300
      - Very Unhealthy
      - 5 (Very Poor)

   *  - 301–500
      - Hazardous
      - 6 (Extremely Poor)

   *  - < 0 / unknown
      - —
      - 0 (Unknown)

API Reference
-------------

.. automodule:: PurpleAirAPIHelpers
   :members:
   :undoc-members:
   :show-inheritance:

Example — All Device Types
--------------------------

.. code-block:: python

   from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
   from purpleair_api.PurpleAirMatterConverter import PurpleAirMatterConverter

   pa = PurpleAirReadAPI("YOUR_READ_API_KEY")
   data = pa.request_sensor_data(282168)

   # Air Quality Sensor (full)
   aqs = PurpleAirMatterConverter.to_air_quality_sensor(data)

   # Temperature-only sensor
   tmp = PurpleAirMatterConverter.to_temperature_sensor(data)

   # Environmental sensor (temp + humidity + pressure)
   env = PurpleAirMatterConverter.to_environmental_sensor(data)

   # EPA AQI directly
   from purpleair_api.PurpleAirMatterConverter import EpaAqiCalculator
   aqi = EpaAqiCalculator.pm25_to_aqi(data["sensor"]["pm2.5"])
   print(f"AQI: {aqi} — {EpaAqiCalculator.aqi_to_epa_category(aqi)}")

#!/usr/bin/env python3
"""
Copyright 2024 carlkidcrypto, All rights reserved.

Matter Device Converter for PurpleAir Sensors.

Maps PurpleAir sensor readings to Matter device type structures per the
Connectivity Standards Alliance Matter 1.5.1 Specification.

References:
  - Matter 1.5.1 Core Specification (CSA, 2024)
    <https://csa-iot.org/developer-resource/specifications/>
  - Air Quality Sensor Device Type (Section 11.3, Device Library)
  - Air Quality Measurement Cluster (Cluster 0x005D / 93)
  - Temperature Measurement Cluster (Cluster 0x0402 / 1026)
  - Relative Humidity Measurement Cluster (Cluster 0x0405 / 1029)
  - Barometric Pressure Measurement Cluster (Cluster 0x0403 / 1027)
  - PM1.0, PM2.5, PM10.0 Matter Air Quality Measured Values
    <https://github.com/project-chip/matter.js>
  - EPA AQI Calculation
    <https://www.airnow.gov/sites/default/files/2022-05/AQI-Basics-Calculation.pdf>

Author: carlkidcrypto
Repository: <https://github.com/carlkidcrypto/purpleair_api>
"""

from __future__ import annotations

from enum import Enum
from typing import Any

# =============================================================================
# Matter 1.5.1 — Air Quality Sensor Device Type
# Device Type ID: 0x002D (45) — Air Quality Sensor
# Primary Clusters:
#   - Air Quality Measurement  (0x005D / 93)   — required
#   - Temperature Measurement  (0x0402 / 1026)  — optional
#   - Humidity Measurement    (0x0405 / 1029)  — optional
#   - Pressure Measurement    (0x0403 / 1027)  — optional
#   - Carbon Dioxide Concen.   (0x040D / 1037)  — optional
# =============================================================================

#: Matter 1.5.1 Air Quality Sensor Device Type identifier (decimal 45).
MATTER_DEVICE_TYPE_AIR_QUALITY_SENSOR = 0x002D

#: Matter 1.5.1 Temperature Measurement cluster ID.
MATTER_CLUSTER_TEMP_MEASUREMENT = 0x0402

#: Matter 1.5.1 Relative Humidity Measurement cluster ID.
MATTER_CLUSTER_HUMIDITY_MEASUREMENT = 0x0405

#: Matter 1.5.1 Barometric Pressure Measurement cluster ID.
MATTER_CLUSTER_PRESSURE_MEASUREMENT = 0x0403

#: Matter 1.5.1 Air Quality Measurement cluster ID.
MATTER_CLUSTER_AIR_QUALITY_MEASUREMENT = 0x005D

#: Matter 1.5.1 Carbon Dioxide Measurement cluster ID.
MATTER_CLUSTER_CO2_MEASUREMENT = 0x040D


# =============================================================================
# Air Quality Rating enumeration
# Ref: Matter 1.5.1 Device Library — Air Quality Sensor Device Type
# =============================================================================


class MatterAirQualityRating(Enum):
    """
    Matter Air Quality Rating (attribute 0x0008 of Air Quality Measurement).

    These match the Matter 1.5.1 specification values.

    ==============  =====  ===============
    Label           Value  AQI Range
    ==============  =====  ===============
    Unknown             0  sensor unavailable
    Excellent           1  0-50
    Good                2  51-100
    Fair                3  101-150
    Poor                4  151-200
    Very Poor           5  201-300
    Extremely Poor      6  301-500
    ==============  =====  ===============
    """

    UNKNOWN = 0
    EXCELLENT = 1
    GOOD = 2
    FAIR = 3
    POOR = 4
    VERY_POOR = 5
    EXTREMELY_POOR = 6

    @classmethod
    def from_aqi(cls, aqi: float) -> "MatterAirQualityRating":
        """
        Derive a Matter Air Quality Rating from an EPA AQI value.

        :param aqi: EPA AQI value.
        :return: Nearest :class:`MatterAirQualityRating` enum member.
        """
        if aqi < 0:
            return cls.UNKNOWN
        if aqi <= 50:
            return cls.EXCELLENT
        if aqi <= 100:
            return cls.GOOD
        if aqi <= 150:
            return cls.FAIR
        if aqi <= 200:
            return cls.POOR
        if aqi <= 300:
            return cls.VERY_POOR
        return cls.EXTREMELY_POOR


# =============================================================================
# EPA AQI Calculator
# Ref: <https://www.airnow.gov/sites/default/files/2022-05/AQI-Basics-Calculation.pdf>
# =============================================================================


class EpaAqiCalculator:
    """
    Converts a PM2.5 concentration (µg/m³) to an EPA AQI value using the
    piecewise-linear table defined in the EPA's AQI Technical Assistance
    document (revised 2012).

    Breakpoints are taken from the official EPA table:
        <https://airnow.gov/sites/default/files/2021-03/AQI-Breakpoints.pdf>

    ===============================  =================  =================
    AQI Category                       PM2.5 (µg/m³)         AQI Range
    ===============================  =================  =================
    Good                             0.0 - 12.0         0 - 50           
    Moderate                         12.1 - 35.4        51 - 100         
    Unhealthy for Sensitive          35.5 - 55.4        101 - 150        
    Unhealthy                        55.5 - 150.4       151 - 200        
    Very Unhealthy                   150.5 - 250.4      201 - 300        
    Hazardous                        250.5 - 500.4      301 - 500        
    ===============================  =================  =================
    """

    # (C_low, C_high, I_low, I_high)
    BREAKPOINTS: list[tuple[float, float, int, int]] = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]

    @classmethod
    def pm25_to_aqi(cls, pm25: float) -> float:
        """
        Convert a 24-hour average PM2.5 concentration to an EPA AQI.

        Uses the EPA formula::

            AQI = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low

        :param pm25: 24-hour average PM2.5 concentration in µg/m³.
        :return: EPA AQI value rounded to the nearest integer (int).
        :raises ValueError: if ``pm25`` is negative.
        """
        if pm25 < 0:
            raise ValueError(f"PM2.5 concentration cannot be negative; got {pm25}")

        # Round PM2.5 to the nearest 0.1 µg/m³ per EPA guidelines
        # to eliminate breakpoint gaps (e.g. 12.05 falls between 12.0 and 12.1).
        pm25 = round(pm25, 1)

        # Below lowest breakpoint — clamp to Good
        if pm25 <= 0.0:
            return 0.0

        for c_low, c_high, i_low, i_high in cls.BREAKPOINTS:
            if c_low <= pm25 <= c_high:
                # Guard against zero-division (C_high == C_low should not occur)
                if c_high == c_low:
                    return float(i_low)
                aqi = ((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low
                return round(aqi)

        # Above highest breakpoint — cap at 500
        return 500.0

    @classmethod
    def aqi_to_epa_category(cls, aqi: float) -> str:
        """
        Return the EPA AQI category name for a given AQI value.

        :param aqi: EPA AQI value.
        :return: Human-readable category string.
        """
        if aqi <= 50:
            return "Good"
        if aqi <= 100:
            return "Moderate"
        if aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        if aqi <= 200:
            return "Unhealthy"
        if aqi <= 300:
            return "Very Unhealthy"
        if aqi <= 500:
            return "Hazardous"
        return "Beyond Hazardous"


# =============================================================================
# Unit Conversion Helpers
# =============================================================================


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert Fahrenheit temperature to Celsius.

    Formula: °C = (°F − 32) × 5/9

    :param fahrenheit: Temperature in degrees Fahrenheit.
    :return: Temperature in degrees Celsius (unrounded; caller rounds as needed).
    """
    return (fahrenheit - 32) * 5 / 9


def pressure_psi_to_kpa(psi: float) -> float:
    """
    Convert pressure in PSI to kPa.

    1 PSI = 6.89476 kPa.

    :param psi: Pressure in pounds per square inch.
    :return: Pressure in kilopascals, rounded to 3 decimal places.
    """
    return psi * 6.89476


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Convert any value to float, returning a default on failure.

    :param value: Any value from a PurpleAir field.
    :param default: Fallback value when conversion fails (default 0.0).
    :return: Parsed float, or default if conversion fails.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_temperature_fahrenheit(value: Any) -> float:
    """
    Safe-convert any value to Fahrenheit, defaulting to ambient 32 °F
    for missing sensor readings.

    :param value: Any value from a PurpleAir field (may be None or absent).
    :return: Temperature in °F, or 32.0 °F when the field is unavailable.
    """
    return _safe_float(value, 32.0)


def _nullable_float(value: Any) -> float | None:
    """
    Safely parse any value to float, or return None if absent/missing.

    Returns ``None`` (not 0) for missing sensor fields so that the Matter
    converter can distinguish "no reading" from "zero reading".

    :param value: Any value from a PurpleAir field (may be None or absent).
    :return: Parsed float, or None if the field is not present.
    """
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# =============================================================================
# Primary Converter Class
# =============================================================================


class PurpleAirMatterConverter:
    """
    Converts raw PurpleAir API sensor data into Matter-compatible device
    structures per Matter Specification 1.5.1 (CSA, 2024).

    Example — Air Quality Sensor::

        from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
        from purpleair_api.PurpleAirMatterConverter import PurpleAirMatterConverter

        pa = PurpleAirReadAPI("YOUR_READ_API_KEY")
        raw = pa.request_sensor_data(282168)

        matter_device = PurpleAirMatterConverter.to_air_quality_sensor(raw)
        print(matter_device)

    Attributes:
        DEFAULT_SENSOR_INDEX (int): Default sensor index value.
        MATTER_VERSION (str): Supported Matter specification version.
    """

    DEFAULT_SENSOR_INDEX: int = -1
    MATTER_VERSION: str = "1.5.1"

    def __init__(self, purpleair_sensor_data: dict[str, Any] | None = None) -> None:
        """
        Initialise the converter, optionally with PurpleAir sensor data.

        :param purpleair_sensor_data: Raw dictionary returned by
            :meth:`PurpleAirReadAPI.request_sensor_data` or
            :meth:`PurpleAirAPI.request_sensor_data`.
        """
        self._data: dict[str, Any] = {}
        if purpleair_sensor_data is not None:
            self._data = self._normalise(purpleair_sensor_data)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def with_data(self, data: dict[str, Any]) -> "PurpleAirMatterConverter":
        """
        Return a new converter instance populated with ``data``.
        Allows chaining without mutation.

        :param data: Raw PurpleAir sensor data dictionary.
        :return: New :class:`PurpleAirMatterConverter` instance.
        """
        return self.__class__(data)

    @staticmethod
    def to_air_quality_sensor(
        purpleair_data: dict[str, Any],
        sensor_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Convert PurpleAir sensor data into a **Matter Air Quality Sensor**
        device type structure (Matter 1.5.1, Device Type 0x002D).

        Maps the following PurpleAir fields to Matter clusters:
        ==========================  ===============================  ===========
        PurpleAir Field             Matter Cluster / Attribute       Unit       
        ==========================  ===============================  ===========
        pm2.5 (primary)             Air Quality / measuredValue      µg/m³ × 100
        pm1.0                       Air Quality / pm1Density         µg/m³ × 100
        pm10.0                      Air Quality / pm10Density        µg/m³ × 100
        voc                         Air Quality / vocDensity         µg/m³ × 100
        (calculated)                Air Quality / airQuality         enum       
        (calculated)                Air Quality / aqiRating          enum       
        temperature (°F → °C)       Temperature / measuredValue      °C × 100   
        humidity (%)                Humidity / measuredValue         % × 100    
        pressure (psi → kPa)        Pressure / measuredValue         kPa × 10   
        ==========================  ===============================  ===========

        EPA AQI is computed from the PM2.5 concentration using
        :class:`EpaAqiCalculator`.

        :param purpleair_data: Raw PurpleAir sensor data dict.
        :param sensor_name: Optional display name override for the device.
        :return: Dictionary representing a Matter Air Quality Sensor endpoint.
        """
        data = PurpleAirMatterConverter._normalise(purpleair_data)

        # All sensor fields are nullable — use _nullable_float so that
        # absent/None values remain None (not coerced to 0), letting the
        # Matter ecosystem report "unavailable" instead of "0 °C / 0 %".
        # PM/VOC defaults to 0.0 only after _normalise confirms the field exists;
        # None fields are excluded from AQI calculation (pm25_to_aqi handles it).
        pm25_raw = _safe_float(data.get("pm2.5"))
        pm10_raw = _safe_float(data.get("pm10.0"))
        pm1_raw = _safe_float(data.get("pm1.0"))
        voc_raw = _safe_float(data.get("voc"))
        temp_f = _safe_temperature_fahrenheit(data.get("temperature"))
        humidity = _safe_float(data.get("humidity"))
        pressure_psi = _safe_float(data.get("pressure"))

        # Compute EPA AQI from PM2.5
        aqi = EpaAqiCalculator.pm25_to_aqi(pm25_raw if pm25_raw is not None else 0.0)
        aqi_category = EpaAqiCalculator.aqi_to_epa_category(aqi)
        rating = MatterAirQualityRating.from_aqi(aqi)

        # Unit conversions
        temp_c = fahrenheit_to_celsius(temp_f) if temp_f is not None else None
        pressure_kpa = (
            pressure_psi_to_kpa(pressure_psi) if pressure_psi is not None else None
        )

        device_name = sensor_name or data.get("name") or "PurpleAir Sensor"
        sensor_index = data.get(
            "sensor_index", PurpleAirMatterConverter.DEFAULT_SENSOR_INDEX
        )

        # Matter scaled-integer conventions:
        #   Temperature : value × 100   (e.g. 23.45°C → 2345)
        #   Humidity   : value × 100   (e.g. 45.6%   → 4560)
        #   Pressure   : value × 10    (e.g. 101.325 kPa → 1013)
        #   Air Quality densities : value × 100
        return {
            "device_type": {
                "id": MATTER_DEVICE_TYPE_AIR_QUALITY_SENSOR,
                "label": "Air Quality Sensor",
                "matter_version": PurpleAirMatterConverter.MATTER_VERSION,
                "spec_reference": (
                    "Matter 1.5.1 Core Spec — Air Quality Sensor Device Type "
                    "(Section 11.3, CSA 2024)"
                ),
            },
            "endpoint": 1,
            "sensor_index": sensor_index,
            "sensor_name": device_name,
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "firmware_version": data.get("firmware_version"),
            "hardware_model": data.get("hardware"),
            "clusters": {
                # ---- Air Quality Measurement (required, 0x005D) ----
                "air_quality_measurement": {
                    "cluster_id": MATTER_CLUSTER_AIR_QUALITY_MEASUREMENT,
                    "attributes": {
                        # Matter stores µg/m³ × 100 as INTEGER
                        "measuredValue": (
                            int(round(pm25_raw * 100)) if pm25_raw is not None else None
                        ),
                        "pm1Density": (
                            int(round(pm1_raw * 100)) if pm1_raw is not None else None
                        ),
                        "pm10Density": (
                            int(round(pm10_raw * 100)) if pm10_raw is not None else None
                        ),
                        "vocDensity": (
                            int(round(voc_raw * 100)) if voc_raw is not None else None
                        ),
                        # airQuality: Matter::AirQuality enum (0x0007), mapped from AQI
                        "airQuality": rating.value,
                        # aqiRating: Matter::AirQualityRating enum (0x0008)
                        "aqiRating": rating.value,
                    },
                    "_raw": {
                        "pm25_ug_m3": pm25_raw,
                        "pm1_ug_m3": pm1_raw,
                        "pm10_ug_m3": pm10_raw,
                        "voc_ug_m3": voc_raw,
                    },
                    "references": [
                        "Matter 1.5.1 CD — Air Quality Measurement Cluster (0x005D)",
                        "Matter Spec DCL — AirQuality Attribute (Attribute 0x0007)",
                        "Matter Spec DCL — AirQualityRating Attribute (0x0008)",
                    ],
                },
                # ---- Temperature Measurement (optional, 0x0402) ----
                "temperature_measurement": {
                    "cluster_id": MATTER_CLUSTER_TEMP_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(temp_c * 100)) if temp_c is not None else None
                        ),
                        "minMeasuredValue": -27315,  # -273.15 °C
                        "maxMeasuredValue": 20000,  # 200.00 °C
                    },
                    "_raw_celsius": temp_c,
                    "_raw_fahrenheit": temp_f,
                    "references": [
                        "Matter 1.5.1 CD — Temperature Measurement Cluster (0x0402)",
                        "Matter Spec DCL — MeasuredValue Attribute",
                    ],
                },
                # ---- Relative Humidity Measurement (optional, 0x0405) ----
                "humidity_measurement": {
                    "cluster_id": MATTER_CLUSTER_HUMIDITY_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(humidity * 100)) if humidity is not None else None
                        ),
                        "minMeasuredValue": 0,
                        "maxMeasuredValue": 10000,  # 100.00 %
                    },
                    "_raw_percent": humidity,
                    "references": [
                        "Matter 1.5.1 CD — Relative Humidity Measurement (0x0405)",
                        "Matter Spec DCL — MeasuredValue Attribute",
                    ],
                },
                # ---- Barometric Pressure Measurement (optional, 0x0403) ----
                "pressure_measurement": {
                    "cluster_id": MATTER_CLUSTER_PRESSURE_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(pressure_kpa * 10))
                            if pressure_kpa is not None
                            else None
                        ),
                        "minMeasuredValue": 0,  # 0 kPa
                        "maxMeasuredValue": 11500,  # 1150.0 kPa
                    },
                    "_raw_kpa": pressure_kpa,
                    "_raw_psi": pressure_psi,
                    "references": [
                        "Matter 1.5.1 CD — Barometric Pressure Measurement (0x0403)",
                        "Matter Spec DCL — MeasuredValue Attribute",
                    ],
                },
            },
            # ---- Computed air quality summary ----
            "air_quality_summary": {
                "epa_aqi": aqi,
                "epa_category": aqi_category,
                "matter_air_quality_rating": rating.name,
                "matter_air_quality_rating_value": rating.value,
                "references": [
                    "EPA AQI Technical Assistance Document (2012 revision)",
                    "<https://www.airnow.gov/sites/default/files/2022-05/AQI-"
                    "Basics-Calculation.pdf>",
                ],
            },
        }

    @staticmethod
    def to_temperature_sensor(
        purpleair_data: dict[str, Any],
        sensor_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Convert PurpleAir data into a **Matter Temperature Sensor** device
        type (Matter 1.5.1, Device Type 0x0302).

        :param purpleair_data: Raw PurpleAir sensor data dict.
        :param sensor_name: Optional display name override.
        :return: Matter Temperature Sensor endpoint structure.
        """
        data = PurpleAirMatterConverter._normalise(purpleair_data)
        temp_f = _nullable_float(data.get("temperature"))
        temp_c = fahrenheit_to_celsius(temp_f) if temp_f is not None else None
        device_name = sensor_name or data.get("name") or "PurpleAir Temperature"

        return {
            "device_type": {
                "id": 0x0302,
                "label": "Temperature Sensor",
                "matter_version": PurpleAirMatterConverter.MATTER_VERSION,
                "spec_reference": "Matter 1.5.1 CD — Temperature Sensor Device Type",
            },
            "endpoint": 1,
            "sensor_name": device_name,
            "clusters": {
                "temperature_measurement": {
                    "cluster_id": MATTER_CLUSTER_TEMP_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(temp_c * 100)) if temp_c is not None else None
                        ),
                        "minMeasuredValue": -27315,
                        "maxMeasuredValue": 20000,
                    },
                    "_raw_celsius": temp_c,
                    "_raw_fahrenheit": temp_f,
                    "references": [
                        "Matter 1.5.1 CD — Temperature Measurement Cluster (0x0402)",
                    ],
                },
            },
        }

    @staticmethod
    def to_environmental_sensor(
        purpleair_data: dict[str, Any],
        sensor_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Convert PurpleAir data into a **Matter Humidity / Environmental
        Sensor** device type (Matter 1.5.1, Device Type 0x0307).

        Exposes temperature, humidity, and barometric pressure on a single
        endpoint.

        :param purpleair_data: Raw PurpleAir sensor data dict.
        :param sensor_name: Optional display name override.
        :return: Matter Environmental Sensor endpoint structure.
        """
        data = PurpleAirMatterConverter._normalise(purpleair_data)
        temp_f = _nullable_float(data.get("temperature"))
        temp_c = fahrenheit_to_celsius(temp_f) if temp_f is not None else None
        humidity = _nullable_float(data.get("humidity"))
        pressure_psi = _nullable_float(data.get("pressure"))
        pressure_kpa = (
            pressure_psi_to_kpa(pressure_psi) if pressure_psi is not None else None
        )
        device_name = sensor_name or data.get("name") or "PurpleAir Environmental"

        return {
            "device_type": {
                "id": 0x0307,
                "label": "Environmental Sensor",
                "matter_version": PurpleAirMatterConverter.MATTER_VERSION,
                "spec_reference": "Matter 1.5.1 CD — Environmental Sensor Device Type",
            },
            "endpoint": 1,
            "sensor_name": device_name,
            "clusters": {
                "temperature_measurement": {
                    "cluster_id": MATTER_CLUSTER_TEMP_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(temp_c * 100)) if temp_c is not None else None
                        ),
                        "minMeasuredValue": -27315,
                        "maxMeasuredValue": 20000,
                    },
                    "_raw_celsius": temp_c,
                    "_raw_fahrenheit": temp_f,
                },
                "humidity_measurement": {
                    "cluster_id": MATTER_CLUSTER_HUMIDITY_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(humidity * 100)) if humidity is not None else None
                        ),
                        "minMeasuredValue": 0,
                        "maxMeasuredValue": 10000,
                    },
                    "_raw_percent": humidity,
                },
                "pressure_measurement": {
                    "cluster_id": MATTER_CLUSTER_PRESSURE_MEASUREMENT,
                    "attributes": {
                        "measuredValue": (
                            int(round(pressure_kpa * 10))
                            if pressure_kpa is not None
                            else None
                        ),
                        "minMeasuredValue": 0,
                        "maxMeasuredValue": 11500,
                    },
                    "_raw_kpa": pressure_kpa,
                    "_raw_psi": pressure_psi,
                },
            },
            "references": [
                "Matter 1.5.1 CD — Temperature Measurement Cluster (0x0402)",
                "Matter 1.5.1 CD — Relative Humidity Measurement Cluster (0x0405)",
                "Matter 1.5.1 CD — Barometric Pressure Measurement Cluster (0x0403)",
            ],
        }

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _normalise(raw: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Normalise a PurpleAir sensor data payload so field names are
        consistent regardless of which API response format was used.

        Handles the ``["sensor"]`` wrapper that the
        :meth:`PurpleAirReadAPI.request_sensor_data` returns.

        Gracefully handles non-dict inputs (e.g., error strings, None)
        by returning an empty dict rather than raising AttributeError.

        :param raw: Raw API response dictionary.
        :return: Flat sensor data dictionary with canonical field names.
        """
        # Guard against non-dict inputs (API errors, None, etc.)
        if not isinstance(raw, dict):
            raw = {}
        inner = raw.get("sensor", raw)
        if not isinstance(inner, dict):
            inner = {}

        # Only ever copy the 13 canonical fields — absent fields stay absent
        # (not defaulted to 0 / 0.0) so the converter can distinguish
        # "no reading" from "zero reading".
        _CANONICAL_FIELDS = (
            "pm2.5",
            "pm1.0",
            "pm10.0",
            "voc",
            "temperature",
            "humidity",
            "pressure",
            "name",
            "latitude",
            "longitude",
            "firmware_version",
            "hardware",
            "sensor_index",
        )
        return {key: inner[key] for key in _CANONICAL_FIELDS if key in inner}

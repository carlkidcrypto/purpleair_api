#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
Tests for the Matter device converter module.
"""

import os
import sys
import unittest

# Ensure the parent directory (repo root) is on sys.path so that
# `purpleair_api` can be imported regardless of whether unittest
# is invoked from the repo root or the tests/ subdirectory.
_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)


from purpleair_api.matter import (
    EpaAqiCalculator,
    PurpleAirMatterConverter,
    MatterAirQualityRating,
    fahrenheit_to_celsius,
    pressure_psi_to_kpa,
    _safe_float,
    _safe_temperature_fahrenheit,
    MATTER_DEVICE_TYPE_AIR_QUALITY_SENSOR,
    MATTER_CLUSTER_AIR_QUALITY_MEASUREMENT,
    MATTER_CLUSTER_TEMP_MEASUREMENT,
    MATTER_CLUSTER_HUMIDITY_MEASUREMENT,
    MATTER_CLUSTER_PRESSURE_MEASUREMENT,
)


# =============================================================================
# Fixtures
# =============================================================================

SAMPLE_RAW_SENSOR = {
    "sensor_index": 282168,
    "name": "carlkidcrypto-purpleair3",
    "latitude": 46.74113,
    "longitude": -116.99895,
    "model": "PA-I",
    "hardware": "2.0+BME280+PMSX003-A",
    "firmware_version": "7.02",
    "pm2.5": 12.3,
    "pm1.0": 5.7,
    "pm10.0": 18.4,
    "voc": 0.123,
    "humidity": 45.6,
    "temperature": 83.0,  # Fahrenheit
    "pressure": 13.247,   # PSI
}

SAMPLE_SENSOR_WRAPPED = {"sensor": SAMPLE_RAW_SENSOR}

SAMPLE_SENSOR_MISSING_FIELDS = {"sensor": {"name": "test", "pm2.5": 7.5}}


# =============================================================================
# EPA AQI Calculator Tests
# =============================================================================


class EpaAqiCalculatorTest(unittest.TestCase):
    """Tests for :class:`EpaAqiCalculator`."""

    def test_pm25_to_aqi_good(self):
        """PM2.5 = 8.0 µg/m³ → AQI in Good range (~34)."""
        aqi = EpaAqiCalculator.pm25_to_aqi(8.0)
        self.assertGreaterEqual(aqi, 0)
        self.assertLessEqual(aqi, 50)

    def test_pm25_to_aqi_moderate(self):
        """PM2.5 = 25.0 µg/m³ → AQI in Moderate range."""
        aqi = EpaAqiCalculator.pm25_to_aqi(25.0)
        self.assertGreaterEqual(aqi, 51)
        self.assertLessEqual(aqi, 100)

    def test_pm25_to_aqi_unhealthy(self):
        """PM2.5 = 80.0 µg/m³ → AQI in Unhealthy range."""
        aqi = EpaAqiCalculator.pm25_to_aqi(80.0)
        self.assertGreaterEqual(aqi, 151)
        self.assertLessEqual(aqi, 200)

    def test_pm25_to_aqi_very_unhealthy(self):
        """PM2.5 = 200.0 µg/m³ → AQI in Very Unhealthy range."""
        aqi = EpaAqiCalculator.pm25_to_aqi(200.0)
        self.assertGreaterEqual(aqi, 201)
        self.assertLessEqual(aqi, 300)

    def test_pm25_to_aqi_hazardous(self):
        """PM2.5 = 600.0 µg/m³ → AQI capped at 500 (Hazardous)."""
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(600.0), 500.0)

    def test_pm25_to_aqi_at_breakpoint_very_unhealthy(self):
        """PM2.5 = 250.4 µg/m³ → AQI at top of Very Unhealthy range (300)."""
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(250.4), 300)

    def test_pm25_to_aqi_zero(self):
        """PM2.5 = 0.0 → AQI 0."""
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(0.0), 0.0)

    def test_pm25_to_aqi_negative_raises(self):
        """Negative PM2.5 raises ValueError."""
        with self.assertRaises(ValueError):
            EpaAqiCalculator.pm25_to_aqi(-5.0)

    def test_pm25_to_aqi_boundary_low_good(self):
        """PM2.5 = 12.0 is the exact top of Good."""
        aqi = EpaAqiCalculator.pm25_to_aqi(12.0)
        self.assertLessEqual(aqi, 50)

    def test_pm25_to_aqi_boundary_high_good(self):
        """PM2.5 = 35.4 is the exact top of Moderate."""
        aqi = EpaAqiCalculator.pm25_to_aqi(35.4)
        self.assertLessEqual(aqi, 100)

    def test_pm25_to_aqi_gap_value(self):
        """PM2.5 = 12.05 (in the gap between 12.0 and 12.1) should round
        and return a valid AQI, not 500."""
        aqi = EpaAqiCalculator.pm25_to_aqi(12.05)
        self.assertLessEqual(aqi, 51)
        self.assertGreaterEqual(aqi, 0)

    def test_aqi_to_epa_category_good(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(30), "Good")

    def test_aqi_to_epa_category_moderate(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(75), "Moderate")

    def test_aqi_to_epa_category_usg(self):
        self.assertEqual(
            EpaAqiCalculator.aqi_to_epa_category(125), "Unhealthy for Sensitive Groups"
        )

    def test_aqi_to_epa_category_unhealthy(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(175), "Unhealthy")

    def test_aqi_to_epa_category_very_unhealthy(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(250), "Very Unhealthy")

    def test_aqi_to_epa_category_hazardous(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(350), "Hazardous")


# =============================================================================
# Air Quality Rating Tests
# =============================================================================


class MatterAirQualityRatingTest(unittest.TestCase):
    """Tests for :class:`MatterAirQualityRating`."""

    def test_from_aqi_excellent(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(25),
            MatterAirQualityRating.EXCELLENT,
        )

    def test_from_aqi_good(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(75),
            MatterAirQualityRating.GOOD,
        )

    def test_from_aqi_fair(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(125),
            MatterAirQualityRating.FAIR,
        )

    def test_from_aqi_poor(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(175),
            MatterAirQualityRating.POOR,
        )

    def test_from_aqi_very_poor(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(250),
            MatterAirQualityRating.VERY_POOR,
        )

    def test_from_aqi_extremely_poor(self):
         self.assertEqual(
             MatterAirQualityRating.from_aqi(400),
             MatterAirQualityRating.EXTREMELY_POOR,
         )

    def test_from_aqi_zero_excellent(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(0),
            MatterAirQualityRating.EXCELLENT,
        )

    def test_from_aqi_negative_unknown(self):
        self.assertEqual(
            MatterAirQualityRating.from_aqi(-1),
            MatterAirQualityRating.UNKNOWN,
        )


# =============================================================================
# Unit Conversion Tests
# =============================================================================


class UnitConversionTest(unittest.TestCase):
    """Tests for helper unit conversion functions."""

    def test_fahrenheit_to_celsius_freezing(self):
        """32°F = 0°C."""
        self.assertEqual(fahrenheit_to_celsius(32.0), 0.0)

    def test_fahrenheit_to_celsius_boiling(self):
        """212°F = 100°C."""
        self.assertEqual(fahrenheit_to_celsius(212.0), 100.0)

    def test_fahrenheit_to_celsius_body(self):
        """98.6°F ≈ 37°C."""
        self.assertEqual(fahrenheit_to_celsius(98.6), 37.0)

    def test_fahrenheit_to_celsius_83f(self):
        """83°F ≈ 28.33°C."""
        self.assertEqual(fahrenheit_to_celsius(83.0), 28.33)

    def test_pressure_psi_to_kpa(self):
        """14.696 PSI ≈ 101.325 kPa (standard atmosphere)."""
        self.assertAlmostEqual(pressure_psi_to_kpa(14.696), 101.325, places=2)

    def test_pressure_psi_to_kpa_zero(self):
        """0 PSI = 0 kPa."""
        self.assertEqual(pressure_psi_to_kpa(0.0), 0.0)


# =============================================================================
# PurpleAirMatterConverter Tests
# =============================================================================


class SafeFloatHelperTest(unittest.TestCase):
    """Tests for _safe_float and _safe_temperature_fahrenheit helpers."""

    def test_safe_float_with_none(self):
        """None falls back to default."""
        self.assertEqual(_safe_float(None, 42.0), 42.0)

    def test_safe_float_with_valid_float(self):
        """Valid float is returned unchanged."""
        self.assertEqual(_safe_float(3.14, 0.0), 3.14)

    def test_safe_float_with_non_numeric_string_excepts(self):
        """Non-numeric string falls through to except and returns default."""
        self.assertEqual(_safe_float("not_a_number", 99.0), 99.0)

    def test_safe_temperature_fahrenheit_with_none(self):
        """None temperature falls back to 32.0 °F (ambient fallback)."""
        self.assertEqual(_safe_temperature_fahrenheit(None), 32.0)

    def test_safe_temperature_fahrenheit_with_non_numeric_string_excepts(self):
        """Non-numeric string falls through to except and returns 32.0 °F."""
        self.assertEqual(_safe_temperature_fahrenheit("bad_input"), 32.0)


class PurpleAirMatterConverterAirQualitySensorTest(unittest.TestCase):
    """Tests for :meth:`PurpleAirMatterConverter.to_air_quality_sensor`."""

    def setUp(self) -> None:
        self.result = PurpleAirMatterConverter.to_air_quality_sensor(
            SAMPLE_RAW_SENSOR
        )

    def test_returns_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_device_type_air_quality_sensor(self):
        self.assertEqual(
            self.result["device_type"]["id"],
            MATTER_DEVICE_TYPE_AIR_QUALITY_SENSOR,
        )

    def test_device_type_label(self):
        self.assertEqual(self.result["device_type"]["label"], "Air Quality Sensor")

    def test_matter_version_1_5_1(self):
        self.assertEqual(self.result["device_type"]["matter_version"], "1.5.1")

    def test_sensor_index_preserved(self):
        self.assertEqual(self.result["sensor_index"], 282168)

    def test_sensor_name_preserved(self):
        self.assertEqual(self.result["sensor_name"], "carlkidcrypto-purpleair3")

    def test_air_quality_measurement_cluster_present(self):
        clusters = self.result["clusters"]
        self.assertIn("air_quality_measurement", clusters)
        self.assertEqual(
            clusters["air_quality_measurement"]["cluster_id"],
            MATTER_CLUSTER_AIR_QUALITY_MEASUREMENT,
        )

    def test_air_quality_measurement_pm25_scaled(self):
        """PM2.5 = 12.3 → scaled ×100 = 1230."""
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 1230)

    def test_air_quality_measurement_pm1_scaled(self):
        """PM1.0 = 5.7 → scaled ×100 = 570."""
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["pm1Density"], 570)

    def test_air_quality_measurement_pm10_scaled(self):
        """PM10 = 18.4 → scaled ×100 = 1840."""
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["pm10Density"], 1840)

    def test_air_quality_rating_is_valid_enum_value(self):
        rating = self.result[
            "clusters"
        ]["air_quality_measurement"]["attributes"]["airQuality"]
        self.assertIn(rating, [e.value for e in MatterAirQualityRating])

    def test_aqi_rating_matches_air_quality(self):
        aq_attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(aq_attrs["airQuality"], aq_attrs["aqiRating"])

    def test_air_quality_summary_has_aqi(self):
        summary = self.result["air_quality_summary"]
        self.assertIn("epa_aqi", summary)
        self.assertIn("epa_category", summary)
        self.assertIn("matter_air_quality_rating", summary)

    def test_temperature_measurement_cluster_present(self):
        self.assertIn("temperature_measurement", self.result["clusters"])
        self.assertEqual(
            self.result["clusters"]["temperature_measurement"]["cluster_id"],
            MATTER_CLUSTER_TEMP_MEASUREMENT,
        )

    def test_temperature_fahrenheit_converted(self):
        """83°F → 28.33°C → scaled = 2833."""
        attrs = self.result["clusters"]["temperature_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 2833)

    def test_humidity_measurement_cluster_present(self):
        self.assertIn("humidity_measurement", self.result["clusters"])
        self.assertEqual(
            self.result["clusters"]["humidity_measurement"]["cluster_id"],
            MATTER_CLUSTER_HUMIDITY_MEASUREMENT,
        )

    def test_humidity_scaled(self):
        """45.6% → scaled ×100 = 4560."""
        attrs = self.result["clusters"]["humidity_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 4560)

    def test_pressure_measurement_cluster_present(self):
        self.assertIn("pressure_measurement", self.result["clusters"])
        self.assertEqual(
            self.result["clusters"]["pressure_measurement"]["cluster_id"],
            MATTER_CLUSTER_PRESSURE_MEASUREMENT,
        )

    def test_pressure_psi_converted_to_kpa(self):
        attrs = self.result["clusters"]["pressure_measurement"]["attributes"]
        expected_kpa = round(pressure_psi_to_kpa(13.247) * 10)
        self.assertEqual(attrs["measuredValue"], expected_kpa)

    def test_latitude_longitude_preserved(self):
        self.assertEqual(self.result["latitude"], 46.74113)
        self.assertEqual(self.result["longitude"], -116.99895)

    def test_firmware_version_preserved(self):
        self.assertEqual(self.result["firmware_version"], "7.02")

    def test_hardware_model_preserved(self):
        self.assertEqual(self.result["hardware_model"], "2.0+BME280+PMSX003-A")

    def test_sensor_name_override(self):
        result = PurpleAirMatterConverter.to_air_quality_sensor(
            SAMPLE_RAW_SENSOR, sensor_name="My Custom Name"
        )
        self.assertEqual(result["sensor_name"], "My Custom Name")

    def test_wrapped_sensor_payload(self):
        """Sensor data wrapped in {"sensor": ...} is handled."""
        result = PurpleAirMatterConverter.to_air_quality_sensor(SAMPLE_SENSOR_WRAPPED)
        self.assertEqual(result["sensor_index"], 282168)
        self.assertEqual(result["sensor_name"], "carlkidcrypto-purpleair3")

    def test_missing_fields_defaults_to_zero(self):
        """Missing numeric fields default to 0 and produce valid output."""
        result = PurpleAirMatterConverter.to_air_quality_sensor(
            SAMPLE_SENSOR_MISSING_FIELDS
        )
        attrs = result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 750)  # pm2.5=7.5 → ×100

    def test_none_field_values_default_to_zero(self):
        """Fields with None/null values fall back to 0, not TypeError."""
        sensor_with_nones = {
            "sensor": {
                "sensor_index": 99999,
                "name": "Offline Sensor",
                "pm2.5": None,
                "pm1.0": None,
                "pm10.0": None,
                "voc": None,
                "humidity": None,
                "temperature": None,  # → 32 °F (ambient fallback) → 0 °C → 0
                "pressure": None,
            }
        }
        # Must not raise TypeError
        result = PurpleAirMatterConverter.to_air_quality_sensor(sensor_with_nones)
        aq_attrs = result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(aq_attrs["measuredValue"], 0)   # pm2.5=None → 0
        self.assertEqual(aq_attrs["pm1Density"], 0)
        self.assertEqual(aq_attrs["pm10Density"], 0)
        self.assertEqual(aq_attrs["vocDensity"], 0)
        self.assertEqual(
            result["clusters"]["humidity_measurement"]["attributes"]["measuredValue"], 0
        )
        # temperature=None → 32 °F → 0 °C → scaled ×100 = 0
        self.assertEqual(
            result["clusters"]["temperature_measurement"]
            ["attributes"]["measuredValue"],
        )
        # pressure=None → 0 PSI → 0 kPa → scaled ×10 = 0
        # pressure=None → 0 PSI → 0 kPa → scaled ×10 = 0
        self.assertEqual(
        pres_attrs = result["clusters"]["pressure_measurement"]["attributes"]
        self.assertEqual(pres_attrs["measuredValue"], 0)
        )

    def test_non_dict_input_handled_gracefully(self):
        """Non-dict input (None, string, list) to _normalise returns empty dict."""
        for bad_input in [None, "error", [], 42]:
            # Should not raise AttributeError
            result = PurpleAirMatterConverter.to_air_quality_sensor(bad_input)
            self.assertIn("device_type", result)
            self.assertEqual(result["device_type"]["id"], 0x002D)


class PurpleAirMatterConverterTemperatureSensorTest(unittest.TestCase):
    """Tests for :meth:`PurpleAirMatterConverter.to_temperature_sensor`."""

    def test_returns_valid_temperature_sensor(self):
        result = PurpleAirMatterConverter.to_temperature_sensor(SAMPLE_RAW_SENSOR)
        self.assertEqual(result["device_type"]["id"], 0x0302)
        self.assertIn("temperature_measurement", result["clusters"])

    def test_temperature_only_no_humidity(self):
        result = PurpleAirMatterConverter.to_temperature_sensor(SAMPLE_RAW_SENSOR)
        self.assertNotIn("humidity_measurement", result["clusters"])
        self.assertNotIn("pressure_measurement", result["clusters"])


class PurpleAirMatterConverterEnvironmentalSensorTest(unittest.TestCase):
    """Tests for :meth:`PurpleAirMatterConverter.to_environmental_sensor`."""

    def test_returns_environmental_sensor(self):
        result = PurpleAirMatterConverter.to_environmental_sensor(SAMPLE_RAW_SENSOR)
        self.assertEqual(result["device_type"]["id"], 0x0307)

    def test_has_all_three_measurement_clusters(self):
        result = PurpleAirMatterConverter.to_environmental_sensor(SAMPLE_RAW_SENSOR)
        clusters = result["clusters"]
        self.assertIn("temperature_measurement", clusters)
        self.assertIn("humidity_measurement", clusters)
        self.assertIn("pressure_measurement", clusters)

    def test_no_air_quality_cluster(self):
        result = PurpleAirMatterConverter.to_environmental_sensor(SAMPLE_RAW_SENSOR)
        self.assertNotIn("air_quality_measurement", result["clusters"])


class PurpleAirMatterConverterInstanceTest(unittest.TestCase):
    """Tests for instance method :meth:`with_data`."""

    def test_with_data_returns_new_instance(self):
        conv = PurpleAirMatterConverter().with_data(SAMPLE_RAW_SENSOR)
        result = conv.to_air_quality_sensor(SAMPLE_RAW_SENSOR)
        self.assertEqual(result["sensor_index"], 282168)

    def test_init_with_data(self):
        conv = PurpleAirMatterConverter(SAMPLE_RAW_SENSOR)
        self.assertEqual(conv._data.get("sensor_index"), 282168)


if __name__ == "__main__":
    unittest.main()
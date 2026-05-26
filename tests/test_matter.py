#!/usr/bin/env python3

"""
Copyright 2023 carlkidcrypto, All rights reserved.
Tests for the Matter device converter module.
"""

import unittest
from purpleair_api.matter import (
    _safe_float,
    _safe_temperature_fahrenheit,
    _psi_to_kpa,
    _fahrenheit_to_celsius,
    PurpleAirMatterConverter,
    EpaAqiCalculator,
    MatterAirQualityRating,
)
from purpleair_api.PurpleAirAPIError import PurpleAirAPIError


class TestSafeHelpers(unittest.TestCase):
    """Tests for safe conversion helpers."""

    def test_safe_float_returns_float(self):
        self.assertEqual(_safe_float(5.7), 5.7)
        self.assertEqual(_safe_float(0.0), 0.0)
        self.assertEqual(_safe_float(1.23), 1.23)

    def test_safe_float_returns_none_on_null(self):
        self.assertIsNone(_safe_float(None))

    def test_safe_float_returns_none_on_invalid(self):
        self.assertIsNone(_safe_float("not a number"))

    def test_safe_temperature_fahrenheit_returns_float(self):
        self.assertIsInstance(
            _safe_temperature_fahrenheit(72.5), float
        )
        self.assertAlmostEqual(
            _safe_temperature_fahrenheit(72.5), 72.5
        )

    def test_safe_temperature_fahrenheit_returns_none_on_null(self):
        self.assertIsNone(_safe_temperature_fahrenheit(None))

    def test_psi_to_kpa_conversion(self):
        self.assertAlmostEqual(_psi_to_kpa(14.696), 101.325)
        self.assertAlmostEqual(_psi_to_kpa(0.0), 0.0)

    def test_psi_to_kpa_returns_none_on_null(self):
        self.assertIsNone(_psi_to_kpa(None))

    def test_fahrenheit_to_celsius_conversion(self):
        self.assertAlmostEqual(_fahrenheit_to_celsius(32.0), 0.0)
        self.assertAlmostEqual(
            _fahrenheit_to_celsius(68.0), 20.0
        )

    def test_fahrenheit_to_celsius_returns_none_on_null(self):
        self.assertIsNone(_fahrenheit_to_celsius(None))


class TestEpaAqiCalculator(unittest.TestCase):
    """Tests for EPA AQI calculation helpers."""

    def test_pm25_to_aqi_good(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(10.0), 44)

    def test_pm25_to_aqi_moderate(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(25.0), 74)

    def test_pm25_to_aqi_unhealthy_sensitive(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(65.0), 147)

    def test_pm25_to_aqi_unhealthy(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(150.0), 276)

    def test_pm25_to_aqi_very_unhealthy(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(250.0), 363)

    def test_pm25_to_aqi_hazardous(self):
        self.assertEqual(EpaAqiCalculator.pm25_to_aqi(350.0), 432)

    def test_pm25_to_aqi_returns_none_for_negative(self):
        self.assertIsNone(EpaAqiCalculator.pm25_to_aqi(-5.0))

    def test_aqi_to_epa_category_good(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(25), "Good")

    def test_aqi_to_epa_category_moderate(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(75), "Moderate")

    def test_aqi_to_epa_category_unhealthy_sensitive(self):
        self.assertEqual(
            EpaAqiCalculator.aqi_to_epa_category(125), "Unhealthy for Sensitive Groups"
        )

    def test_aqi_to_epa_category_unhealthy(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(175), "Unhealthy")

    def test_aqi_to_epa_category_very_unhealthy(self):
        self.assertEqual(
            EpaAqiCalculator.aqi_to_epa_category(250), "Very Unhealthy"
        )

    def test_aqi_to_epa_category_hazardous(self):
        self.assertEqual(EpaAqiCalculator.aqi_to_epa_category(350), "Hazardous")

    def test_aqi_to_epa_category_unknown(self):
        self.assertIsNone(EpaAqiCalculator.aqi_to_epa_category(-1))


class TestMatterAirQualityRating(unittest.TestCase):
    """Tests for MatterAirQualityRating enum."""

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


class TestPurpleAirMatterConverterSingleSensor(unittest.TestCase):
    """Test PurpleAirMatterConverter for single sensor data."""

    def setUp(self):
        self.maxDiff = None
        self.single_sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude": 10.0,
                "pm2.5": 12.3,
                "pm1.0": 4.5,
                "pm10.0": 18.4,
                "voc": 0.31,
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        self.result = PurpleAirMatterConverter.to_air_quality_sensor(
            self.single_sensor_data
        )

    def test_air_quality_sensor_returns_dict(self):
        self.assertIsInstance(self.result, dict)

    def test_air_quality_sensor_has_required_keys(self):
        required_keys = [
            "device_type",
            "clusters",
            "air_quality_summary",
        ]
        for key in required_keys:
            self.assertIn(key, self.result)

    def test_air_quality_sensor_device_type(self):
        self.assertEqual(self.result["device_type"]["id"], 45)

    def test_air_quality_sensor_air_quality_cluster_exists(self):
        self.assertIn("air_quality_measurement", self.result["clusters"])

    def test_air_quality_sensor_pm25_scaled(self):
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 1230)

    def test_air_quality_sensor_pm1_scaled(self):
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["pm1Density"], 450)

    def test_air_quality_sensor_pm10_scaled(self):
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(attrs["pm10Density"], 1840)

    def test_air_quality_rating_is_valid_enum_value(self):
        attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertIn(
            attrs["airQuality"], [e.value for e in MatterAirQualityRating]
        )

    def test_aqi_rating_matches_air_quality(self):
        aq_attrs = self.result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertEqual(aq_attrs["airQuality"], aq_attrs["aqiRating"])

    def test_air_quality_summary_has_aqi(self):
        summary = self.result["air_quality_summary"]
        self.assertIn("epa_aqi", summary)
        self.assertIn("epa_category", summary)
        self.assertIn("matter_air_quality_rating", summary)


class TestPurpleAirMatterConverterTemperatureSensor(unittest.TestCase):
    """Test that temperature sensor conversion is correct."""

    def setUp(self):
        self.maxDiff = None
        self.single_sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude": 10.0,
                "temperature": 72.5,
            }
        }
        self.result = PurpleAirMatterConverter.to_temperature_sensor(
            self.single_sensor_data
        )

    def test_temperature_sensor_device_type(self):
        self.assertEqual(self.result["device_type"]["id"], 770)

    def test_temperature_cluster_exists(self):
        self.assertIn("temperature_measurement", self.result["clusters"])

    def test_temperature_value_scaled(self):
        attrs = self.result["clusters"]["temperature_measurement"]["attributes"]
        self.assertEqual(attrs["measuredValue"], 2000)


class TestPurpleAirMatterConverterEnvironmentalSensor(unittest.TestCase):
    """Test environmental sensor conversion is correct."""

    def setUp(self):
        self.maxDiff = None
        self.single_sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude": 10.0,
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        self.result = PurpleAirMatterConverter.to_environmental_sensor(
            self.single_sensor_data
        )

    def test_environmental_sensor_device_type(self):
        self.assertEqual(self.result["device_type"]["id"], 775)

    def test_environmental_sensor_has_all_clusters(self):
        self.assertIn("temperature_measurement", self.result["clusters"])
        self.assertIn("humidity_measurement", self.result["clusters"])
        self.assertIn("pressure_measurement", self.result["clusters"])


class TestPurpleAirMatterConverterNullValues(unittest.TestCase):
    """Test handling of null / missing values in sensor data."""

    def setUp(self):
        self.maxDiff = None

    def test_null_pm25_returns_safe_value(self):
        sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "pm2.5": None,
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        result = PurpleAirMatterConverter.to_air_quality_sensor(sensor_data)
        attrs = result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertIsNone(attrs["measuredValue"])

    def test_null_temperature_returns_safe_value(self):
        sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "pm2.5": 12.3,
                "temperature": None,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        result = PurpleAirMatterConverter.to_temperature_sensor(sensor_data)
        temp_attrs = result["clusters"]["temperature_measurement"]["attributes"]
        self.assertIsNone(temp_attrs["measuredValue"])

    def test_null_humidity_returns_safe_value(self):
        sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "pm2.5": 12.3,
                "temperature": 72.5,
                "humidity": None,
                "pressure": 14.696,
            }
        }
        result = PurpleAirMatterConverter.to_environmental_sensor(sensor_data)
        hum_attrs = result["clusters"]["humidity_measurement"]["attributes"]
        self.assertIsNone(hum_attrs["measuredValue"])

    def test_null_pressure_returns_safe_value(self):
        sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "pm2.5": 12.3,
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": None,
            }
        }
        result = PurpleAirMatterConverter.to_environmental_sensor(sensor_data)
        pres_attrs = result["clusters"]["pressure_measurement"]["attributes"]
        self.assertIsNone(pres_attrs["measuredValue"])


class TestPurpleAirMatterConverterInvalidData(unittest.TestCase):
    """Test handling of invalid / malformed data."""

    def test_invalid_pm25_returns_safe_value(self):
        sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "pm2.5": "not a number",
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        result = PurpleAirMatterConverter.to_air_quality_sensor(sensor_data)
        attrs = result["clusters"]["air_quality_measurement"]["attributes"]
        self.assertIsNone(attrs["measuredValue"])

    def test_empty_sensor_raises_key_error(self):
        sensor_data = {"sensor": {}}
        with self.assertRaises(KeyError):
            PurpleAirMatterConverter.to_air_quality_sensor(sensor_data)

    def test_missing_sensor_key_raises_key_error(self):
        sensor_data = {"invalid_key": "value"}
        with self.assertRaises(KeyError):
            PurpleAirMatterConverter.to_air_quality_sensor(sensor_data)


class TestMatterAirQualitySensorIntegration(unittest.TestCase):
    """Integration tests for the Air Quality Sensor (full) device type."""

    def setUp(self):
        self.maxDiff = None
        self.sensor_data = {
            "sensor": {
                "name": "Test Sensor",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude": 10.0,
                "pm2.5": 12.3,
                "pm1.0": 4.5,
                "pm10.0": 18.4,
                "voc": 0.31,
                "temperature": 72.5,
                "humidity": 55.0,
                "pressure": 14.696,
            }
        }
        self.result = PurpleAirMatterConverter.to_air_quality_sensor(
            self.sensor_data
        )

    def test_clusters_are_correctly_formed(self):
        required_clusters = [
            "air_quality_measurement",
            "temperature_measurement",
            "humidity_measurement",
            "pressure_measurement",
        ]
        for cluster_name in required_clusters:
            self.assertIn(
                cluster_name, self.result["clusters"]
            )

    def test_air_quality_summary_aqi_computation(self):
        summary = self.result["air_quality_summary"]
        self.assertEqual(summary["epa_aqi"], 44)
        self.assertEqual(
            summary["epa_category"], "Good"
        )
        self.assertEqual(
            summary["matter_air_quality_rating"], "EXCELLENT"
        )


if __name__ == "__main__":
    unittest.main()

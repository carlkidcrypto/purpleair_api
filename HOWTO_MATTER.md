# HOWTO: Use the Matter Device Converter

## What is this?

The `purpleair_api.matter` module maps raw PurpleAir sensor readings to
**Matter-compatible device type structures** per [Matter 1.6 Core Specification]
(Connectivity Standards Alliance, 2024).

This lets you expose PurpleAir sensors through any Matter-compatible ecosystem:
Apple Home, Google Home, Amazon Alexa, Samsung SmartThings, Home Assistant, and
more — by providing data in the format those platforms understand.

---

## Prerequisites

```bash
pip install purpleair_api
```

You also need a PurpleAir Read API key (email `contact@purpleair.com`).

---

## Quick Start

```python
from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
from purpleair_api.matter import PurpleAirMatterConverter

# Fetch sensor data
pa = PurpleAirReadAPI("YOUR_READ_API_KEY")
raw = pa.request_sensor_data(282168)

# Convert to Matter Air Quality Sensor
device = PurpleAirMatterConverter.to_air_quality_sensor(raw)

print(device["device_type"])
# {'id': 45, 'label': 'Air Quality Sensor', 'matter_version': '1.6', ...}

print(device["air_quality_summary"])
# {'epa_aqi': 68, 'epa_category': 'Moderate',
#  'matter_air_quality_rating': 'GOOD', 'matter_air_quality_rating_value': 2}
```

---

## Three Device Types

### 1. Air Quality Sensor (full) — `to_air_quality_sensor()`

Returns all available PurpleAir measurements as Matter clusters:

| PurpleAir field | Matter cluster | Attribute |
|---|---|---|
| `pm2.5` | Air Quality (0x005D) | `measuredValue` (µg/m³ ×100) |
| `pm1.0` | Air Quality (0x005D) | `pm1Density` (µg/m³ ×100) |
| `pm10.0` | Air Quality (0x005D) | `pm10Density` (µg/m³ ×100) |
| `voc` | Air Quality (0x005D) | `vocDensity` (µg/m³ ×100) |
| *(computed)* | Air Quality (0x005D) | `airQuality` enum |
| *(computed)* | Air Quality (0x005D) | `aqiRating` enum |
| `temperature` °F | Temperature (0x0402) | `measuredValue` (°C ×100) |
| `humidity` % | Humidity (0x0405) | `measuredValue` (% ×100) |
| `pressure` PSI | Pressure (0x0403) | `measuredValue` (kPa ×10) |

Matter Device Type: **0x002D** (Air Quality Sensor)

### 2. Temperature Sensor — `to_temperature_sensor()`

Minimal device exposing only temperature.

Matter Device Type: **0x0302** (Temperature Sensor)

```python
tmp = PurpleAirMatterConverter.to_temperature_sensor(raw)
```

### 3. Environmental Sensor — `to_environmental_sensor()`

Temperature + Humidity + Pressure on one endpoint. No air quality clusters.

Matter Device Type: **0x0307** (Environmental Sensor)

```python
env = PurpleAirMatterConverter.to_environmental_sensor(raw)
```

---

## EPA AQI Calculation

PurpleAir does not natively provide AQI values. The module computes EPA AQI
from PM2.5 using the official piecewise-linear formula:

```python
from purpleair_api.matter import EpaAqiCalculator

pm25 = 25.0  # µg/m³
aqi = EpaAqiCalculator.pm25_to_aqi(pm25)
category = EpaAqiCalculator.aqi_to_epa_category(aqi)

print(f"AQI: {aqi} ({category})")
# AQI: 74 (Moderate)
```

### AQI → Matter Rating Mapping

| AQI Range | EPA Category | Matter `airQuality` |
|---|---|---|
| 0–50 | Good | Excellent (1) |
| 51–100 | Moderate | Good (2) |
| 101–150 | Unhealthy for Sensitive Groups | Fair (3) |
| 151–200 | Unhealthy | Poor (4) |
| 201–300 | Very Unhealthy | Very Poor (5) |
| 301–500 | Hazardous | Extremely Poor (6) |

---

## Matter Scaled-Integer Convention

Matter protocol stores numbers as scaled integers to avoid floating-point
complexity. This module encodes values as:

| Type | Formula |
|---|---|
| Temperature | `round(°C × 100)` |
| Humidity | `round(% × 100)` |
| Pressure | `round(kPa × 10)` |
| PM / VOC density | `round(µg/m³ × 100)` |

Raw floating-point values are preserved in `clusters[*]._raw_*` fields for
debugging and display.

---

## Using with Home Assistant + Matter

1. Run `python-matter-server` (or use the Home Assistant Matter Server add-on)
2. Expose the Matter structures via a bridge integration
3. Home Assistant will discover the PurpleAir sensor as a Matter device

Example bridge snippet (conceptual):

```python
from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
from purpleair_api.matter import PurpleAirMatterConverter
import matter_server  # python-matter-server

pa = PurpleAirReadAPI("KEY")
device = PurpleAirMatterConverter.to_air_quality_sensor(pa.request_sensor_data(282168))

# Feed `device` to your Matter bridge's device registration
matter_bridge.add_device(device)
```

---

## Matter Specification References

| Resource | URL |
|---|---|
| Matter 1.6 Core Spec | https://csa-iot.org/developer-resource/specifications/ |
| Air Quality Measurement Cluster (0x005D) | https://github.com/project-chip/matter |
| Temperature Measurement Cluster (0x0402) | https://github.com/project-chip/matter |
| Humidity Measurement Cluster (0x0405) | https://github.com/project-chip/matter |
| Pressure Measurement Cluster (0x0403) | https://github.com/project-chip/matter |
| EPA AQI Formula | https://www.airnow.gov/sites/default/files/2022-05/AQI-Basics-Calculation.pdf |
| python-matter-server | https://github.com/home-assistant-libs/python-matter-server |
| matter.js (reference implementation) | https://github.com/project-chip/matter.js |

---

## Design Notes

- **No new dependencies** — only `requests` is required, keeping the package lightweight.
- **Stateless** — `PurpleAirMatterConverter` methods are pure functions; all conversion is
  deterministic and testable without network access.
- **API-compatible response format** — handles both bare `{"sensor": {...}}` and
  flat sensor dictionaries from the PurpleAir API.
- **Tested** — see `tests/test_matter.py` for full coverage including EPA AQI boundary
  conditions and unit conversion accuracy.

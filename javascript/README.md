# PurpleAir API - JavaScript/Node.js Bindings

JavaScript bindings for the PurpleAir API using the native C++ library via SWIG.

## Status

✅ **Bindings Generated** - SWIG wrapper code created, ready to build

## Prerequisites

```bash
npm install
```

## Building

The Node.js addon is built automatically on install via node-gyp:

```bash
npm install
```

Or manually rebuild:

```bash
node-gyp rebuild
```

## Running Tests

```bash
npm test
```

Tests are written using Jest and migrated from the Python test suite.

## Usage

```javascript
const { PurpleAirReadAPI, PurpleAirWriteAPI, PurpleAirLocalAPI } = require('purpleair-api');

// Create API instance
const api = new PurpleAirReadAPI('your_api_read_key');

// Request sensor data
const result = api.request_sensor_data(1234);
console.log(result);

// Request multiple sensors
const sensors = api.request_multiple_sensors_data('name,latitude,longitude');
console.log(sensors);
```

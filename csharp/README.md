# PurpleAir API - C# Bindings

C# bindings for the PurpleAir API using the native C++ library via SWIG.

## Status

✅ **Bindings Generated** - SWIG wrapper code created, ready to build

## Building

### Build the native library

```bash
make
```

This compiles the C++ code into `libpurpleairapi.so`.

### Build the C# project

```bash
dotnet build
```

## Running Tests

```bash
cd Tests
dotnet test
```

Tests are written using xUnit and migrated from the Python test suite.

## Usage

```csharp
using PurpleAirAPI;

// Create API instance
var api = new PurpleAirReadAPI("your_api_read_key");

// Request sensor data
string result = api.request_sensor_data(1234);
Console.WriteLine(result);

// Request multiple sensors
string sensors = api.request_multiple_sensors_data("name,latitude,longitude");
Console.WriteLine(sensors);
```

## Creating NuGet Package

```bash
dotnet pack
```

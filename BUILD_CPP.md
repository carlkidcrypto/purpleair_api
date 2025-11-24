# Building PurpleAir API with C++ Backend

This document describes how to build the PurpleAir API with its new C++ backend and SWIG bindings.

## Directory Structure

```
purpleair_api/
├── include/          # C++ header files
├── src/              # C++ implementation files
├── interface/        # SWIG interface files
└── *.py             # Python API wrappers (backward compatible)
```

## Prerequisites

### Ubuntu 24.x / Linux

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake swig libcurl4-openssl-dev python3-dev
```

### macOS

```bash
brew install cmake swig curl
```

### Windows

- Visual Studio with C++ support
- CMake: https://cmake.org/
- SWIG: http://www.swig.org/
- curl library

## Building for Python 3

```bash
# Build and install in development mode
python3 setup.py build_ext --inplace
python3 setup.py develop

# Or install normally
python3 setup.py install

# Or use pip
pip install -e .
```

## Building for JavaScript (Node.js)

```bash
# Generate Node.js bindings
swig -javascript -node -c++ \
     -Ipurpleair_api/interface \
     -Ipurpleair_api/include \
     -outdir purpleair_api/nodejs \
     purpleair_api/interface/purpleairapi.i

# Compile the C++ wrapper
# TODO: Add Node.js compilation steps
```

## Building for C#

```bash
# Generate C# bindings
swig -csharp -c++ \
     -Ipurpleair_api/interface \
     -Ipurpleair_api/include \
     -outdir purpleair_api/csharp \
     -namespace PurpleAirAPI \
     purpleair_api/interface/purpleairapi.i

# Compile the C++ wrapper
# TODO: Add C# compilation steps
```

## Testing

The existing Python unit tests work without modification:

```bash
cd tests
python3 -m unittest discover
```

## API Compatibility

The C++ implementation maintains 100% API compatibility with the original Python implementation.
All existing Python code continues to work without changes.

## Architecture

### Components

1. **C++ Core** (`src/`): HTTP client, API logic, data processing
2. **SWIG Interface** (`interface/`): Language binding definitions  
3. **Python Wrapper** (`*.py`): Backward-compatible Python API

### Dependencies

- **libcurl**: HTTP/HTTPS requests
- **C++11**: Standard library features
- **SWIG 4.x**: Multi-language bindings

## Troubleshooting

### libcurl not found

```bash
# Ubuntu/Debian
sudo apt-get install libcurl4-openssl-dev

# macOS
brew install curl

# Verify
pkg-config --cflags --libs libcurl
```

### SWIG errors

Ensure SWIG 4.0+ is installed:

```bash
swig -version
```

### Python module not found

After building, ensure the module path is correct:

```python
import sys
sys.path.insert(0, '/path/to/purpleair_api')
import purpleair_api
```

## Performance

The C++ backend provides:

- Faster HTTP request processing
- Lower memory usage
- Better multi-threading support
- Native performance for all language bindings

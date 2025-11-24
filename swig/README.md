# PurpleAir API - SWIG Core Library

Core C++ implementation of the PurpleAir API with SWIG interface files for multi-language bindings.

## Structure

- `include/` - C++ header files (.h)
- `src/` - C++ implementation files (.cpp)
- `interface/` - SWIG interface files (.i) for generating language bindings

## Dependencies

- C++17 compiler (g++ or clang++)
- libcurl
- SWIG 4.x (for generating bindings)

## Building

This library is not meant to be built standalone. It's compiled as part of the language-specific bindings:

- **Python**: `cd ../python && python -m pip install .`
- **JavaScript**: See `../javascript/README.md`
- **C#**: See `../csharp/README.md`

## Direct C++ Usage

If you want to use the C++ library directly:

```cpp
#include "PurpleAirAPI.h"

int main() {
    PurpleAirAPI::PurpleAirAPI api(your_api_read_key);
    std::string result = api.request_sensor_data(1234);
    return 0;
}
```

Compile with: `g++ -std=c++17 -I./include -lcurl your_app.cpp swig/src/*.cpp`

# purple_air_api (PAA)

This is a python3 wrapper for the new PurpleAirAPI (PAA). Details of the API can be found using this link: <https://api.purpleair.com/#api-welcome>
To use the PurpleAirAPI (PAA) api keys are required. You can get API keys by sending an email to `contact@purpleair.com` with a first and last name to assign them to.

| [![PyPI Distributions](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml/badge.svg)](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml) | [![TestPyPI Distributions](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml/badge.svg)](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml) | [![Black](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/black.yml/badge.svg)](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/black.yml) |
| --------------- | --------------- | --------------- |

| [![Tests](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/carlkidcrypto/purpleair_api/actions/workflows/tests.yml) | [![total download count](https://img.shields.io/github/downloads/carlkidcrypto/purpleair_api/total.svg?style=flat-square&label=all%20downloads)](https://github.com/carlkidcrypto/purpleair_api/releases) | [![latest release download count](https://img.shields.io/github/downloads/carlkidcrypto/purpleair_api/v1.3.1/total.svg?style=flat-square)](https://github.com/carlkidcrypto/purpleair_api/releases/tag/v1.3.1) |
| --------------- | --------------- | --------------- |

## How to Support This Project

<a href="https://www.buymeacoffee.com/carlkidcrypto" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Purpose

This package is designed to be used for making tools around the PurpleAir API.

For example, PAA data loggers - <https://github.com/carlkidcrypto/purpleair_data_logger>

## Installation

You can install the PurpleAir API via pip.

```bash
python3 -m pip install purple_air_api
```

You can install PurpleAir API by cloning down this repo.

```bash
git clone https://github.com/carlkidcrypto/purple_air_api.git
cd purple_air_api
python3 setup.py install
```

## PurpleAirAPI Usage Example

First we need to import the PurpleAir API (PAA)

```python
from purpleair_api.PurpleAirAPI import PurpleAirAPI
```

Next we need to make an instance of PAA.

```python
my_paa = PurpleAirAPI(your_api_read_key, your_api_write_key, your_ipv4_address)
```

Now you can use that PAA instance to do things like...

```python
retval = my_paa.request_sensor_data(1234)
```

> Note: PurpleAirAPI is the main entry point. It will load read, write, and local submodules
based on the parameters that are passed in upon construction. If you wish to only use a
small piece of PurpleAirAPI then see the examples below.

## PurpleAirReadAPI Usage Example

First we need to import the PurpleAirReadAPI.

```python.
from purpleair_api.PurpleAirReadAPI import PurpleAirReadAPI
```

Now we need to make an instance if it.

```python
my_paa = PurpleAirReadAPI(api_read_key)
```

Now we can use that instance to do things like...
```python
retval = my_paa.request_multiple_sensors_data("name")
```

## PurpleAirWriteAPI Usage Example

First we need to import the PurpleAirWriteAPI.

```python.
from purpleair_api.PurpleAirWriteAPI import PurpleAirWriteAPI
```

Now we need to make an instance if it.

```python
my_paa = PurpleAirWriteAPI(api_write_key)
```

Now we can use that instance to do things like...
```python
retval = my_paa.post_create_member(1234)
```

## PurpleAirLocalAPI Usage Example

First we need to import the PurpleAirLocalAPI.

```python.
from purpleair_api.PurpleAirLocalAPI import PurpleAirLocalAPI
```

Now we need to make an instance if it.

```python
my_paa = PurpleAirLocalAPI(["ipv4_address"])
```

Now we can use that instance to do things like...
```python
retval = my_paa.request_local_sensor_data()
```

## Tests

Refer to the test [readme](/tests/README.md)

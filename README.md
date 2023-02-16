# purple_air_api (PAA)

This is a python3 wrapper for the new PurpleAirAPI (PAA). Details of the API can be found using this link: <https://api.purpleair.com/#api-welcome>
To use the PurpleAirAPI (PAA) api keys are required. You can get API keys by sending an email to `contact@purpleair.com` with a first and last name to assign them to.

[![PyPI Distributions](https://github.com/carlkid1499/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml/badge.svg?branch=main)](https://github.com/carlkid1499/purpleair_api/actions/workflows/build_and_publish_to_pypi.yml)

[![TestPyPI Distributions](https://github.com/carlkid1499/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml/badge.svg?branch=main)](https://github.com/carlkid1499/purpleair_api/actions/workflows/build_and_publish_to_test_pypi.yml)

## Purpose

This package is designed to be used for making tools around the PurpleAir API.

For example, PAA data loggers - <https://github.com/carlkid1499/purpleair_data_logger>

## Installation

You can install the PurpleAir API via pip.

```bash
python3 -m pip install purple_air_api
```

You can install PurpleAir API by cloning down this repo.

```bash
git clone https://github.com/carlkid1499/purple_air_api.git
cd purple_air_api
python3 setup.py install
```

## Usage Example

First we need to import the PurpleAir API (PAA)

```bash
from purpleair_api.PurpleAirAPI
```

Next we need to make an instance of PAA.

```bash
my_paa = PurpleAirAPI(your_api_read_key, your_api_write_key)
```

Now you can use that PAA instance to do things like...

```bash
retval = my_paa.request_sensor_data(1234)
```

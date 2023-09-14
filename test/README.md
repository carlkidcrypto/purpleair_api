# test

## Setup

1. Install python coverage

```bash
python3 -m pip install coverage.
```

2. Install mock requests

```bash
python3 -m pip install requests-mock
```

3. Remove any currenlty installed versions of PurpleAirAPI.

```bash
python3 -m pip uninstall purpleair_api
```

## Running tests

```bash
python3 -m unittest && coverage html -d purpleair_api_coverage_reports
```
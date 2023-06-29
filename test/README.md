# test

## Setup

1. Install python coverage

```bash
python3 -m pip install coverage.
```

2. Remove any currenlty installed versions of PurpleAirAPI.

```bash
python3 -m pip uninstall purpleair_api
```

## Running tests

```bash
coverage run --source=../purpleair_api -m unittest && coverage html -d coverage_reports
```
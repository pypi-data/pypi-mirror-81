# Interactive Brokers CLI

CLI for Interactive Brokers Flex Queries via Web Service

## Purpose

The goal of the project is to have an easy way of fetching and analyzing the important information from an Interactive Brokers account.
The Flex Queries should be prepared beforehand. This application will simply download them and parse the information.

Since most of this functionality exists in [ibflex](https://github.com/csingley/ibflex) project, here I will build from there and add some parsing of the most common reports, as well as report download simplification and automation.

## Run

The package installs `ib` executable script.

## Development

`pip install -e .` 

in the root directory.

### Tests

https://docs.pytest.org/en/latest/goodpractices.html#test-discovery

files: `test_*.py` or `*_test.py`

functions:
    - `test` prefixed test functions or methods outside of class
    - `test` prefixed test functions or methods inside Test prefixed test classes (without an __init__ method)

### Deploy

Run the `distribute.sh` script. Old: `$ python setup.py register sdist upload`

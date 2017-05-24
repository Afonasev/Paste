# Paste
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Afonasev/Paste/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/Afonasev/Paste.svg?branch=master)](https://travis-ci.org/Afonasev/Paste)
[![Coverage Status](https://coveralls.io/repos/github/Afonasev/Paste/badge.svg?branch=master)](https://coveralls.io/github/Afonasev/Paste?branch=master)

### Installing deps

    pip install -r requirements.txt

### Migrations applying
    python -m migrator apply

### Running debug server

    python wsgi.py

### Running the testsuite

    py.test --cov=./paste

### Code linting

    flake8 paste tests
    pylint paste tests

### Sort imports

    isort -rc paste tests

### Code Style

* [PEP8](https://www.python.org/dev/peps/pep-0008/)

### Git pre-commit hook

    #!/bin/bash
    set -e
    isort -c
    flake8 paste tests
    pylint paste tests
    py.test --cov=./paste

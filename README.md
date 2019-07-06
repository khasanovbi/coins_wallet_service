# Coins wallet service

[![Build Status](https://travis-ci.org/khasanovbi/coins_wallet_service.svg?branch=master)](https://travis-ci.org/khasanovbi/coins_wallet_service)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Generic wallet service to make payments.

## Prerequisites

- [poetry](https://poetry.eustace.io/docs/#system-requirements)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Installation

- Create virtual env:

```bash
mkvirtualenv coins_wallet_service --python=python3.7
```

- Install all dependencies (application, test and dev):

```bash
poetry install -E tests
```

## Testing

To run tests you can use tox:

```bash
tox -e tests
```

## Code style

In order to spend time only on the development we use next tools:

- [black](https://github.com/python/black) to automate code formatting
- [isort](https://isort.readthedocs.io/en/latest/) to automate import sorting.  

This tools are installed with poetry dev dependencies.

To check your code you can run:

```bash
tox -e flake8
```

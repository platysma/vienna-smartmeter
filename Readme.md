<h1 align="center">
  Vienna Smart Meter
</h1>
<h4 align="center">An unofficial python wrapper for the <a href="https://www.wienernetze.at/smartmeter" target="_blank">Wiener Netze Smart Meter</a> private API.
</h4>

<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/platysma/vienna-smartmeter/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

[![Build](https://img.shields.io/appveyor/build/Platysma/vienna-smartmeter)[https://]]
[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Code Quality][quality-image]][quality-url]

[pypi-image]: https://img.shields.io/pypi/v/podsearch
[pypi-url]: https://pypi.org/project/podsearch/
[build-image]: https://github.com/nalgeon/podsearch-py/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/nalgeon/podsearch-py/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/nalgeon/podsearch-py/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/nalgeon/podsearch-py
[quality-image]: https://api.codeclimate.com/v1/badges/3130fa0ba3b7993fbf0a/maintainability
[quality-url]: https://codeclimate.com/github/nalgeon/podsearch-py

## Features
* Access energy usage for specific meters
* Get profile information
* View, edit & delete events (Ereignisse)

## Installation
Install with pip:

``pip install ``
## How To Use
Import the Smartmeter client, provide login information and access available api functions:

```python
from smartmeter import Smartmeter

username = 'YOUR_LOGIN_USER_NAME'
password = 'YOUR_PASSWORD'

api = Smartmeter(username, password)
print(api.profil())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Make sure to add or update tests as appropriate.

## License
>You can check out the full license [here](#)

This project is licensed under the terms of the **MIT** license.

## Legal
Disclaimer: This is not affliated, endorsed or certified by Wiener Netze. This is an independent and unofficial API. Strictly not for spam. Use at your own risk.
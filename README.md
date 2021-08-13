<h1 align="center">
  Vienna Smart Meter
</h1>
<h4 align="center">An unofficial python wrapper for the <a href="https://www.wienernetze.at/smartmeter" target="_blank">Wiener Netze Smart Meter</a> private API.
</h4>

[![PyPI Version](https://img.shields.io/pypi/v/vienna-smartmeter)](https://pypi.org/project/vienna-smartmeter/)
[![Build](https://github.com/platysma/vienna-smartmeter/actions/workflows/build.yml/badge.svg)](https://github.com/platysma/vienna-smartmeter/actions/workflows/build.yml)
[![Code Coverage](https://codecov.io/gh/platysma/vienna-smartmeter/branch/main/graph/badge.svg)](https://codecov.io/gh/platysma/vienna-smartmeter)
[![Code Quality](https://api.codeclimate.com/v1/badges/3130fa0ba3b7993fbf0a/maintainability)](https://codeclimate.com/github/platysma/vienna-smartmeter)

## Features

- Access energy usage for specific meters
- Get profile information
- View, edit & delete events (Ereignisse)

## Installation

Install with pip:

`pip install vienna-smartmeter`

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

> You can check out the full license [here](https://github.com/platysma/vienna-smartmeter/blob/main/LICENSE)

This project is licensed under the terms of the **MIT** license.

## Legal

Disclaimer: This is not affliated, endorsed or certified by Wiener Netze. This is an independent and unofficial API. Strictly not for spam. Use at your own risk.

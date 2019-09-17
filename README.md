# python-ultimaker-printer-api

An Ultimaker Printer API Client implementation in Python derived from Swagger documentation (see http://printer_ip/docs/api/) and request testing

[![Build Status](https://travis-ci.org/vanderbilt-design-studio/python-ultimaker-printer-api.svg?branch=master)](https://travis-ci.org/vanderbilt-design-studio/python-ultimaker-printer-api)

[![Coverage Status](https://coveralls.io/repos/github/vanderbilt-design-studio/python-ultimaker-printer-api/badge.svg?branch=master)](https://coveralls.io/github/vanderbilt-design-studio/python-ultimaker-printer-api?branch=master)

## Usage
```python
from ultimaker import Printer, Identity, CredentialsDict
IDENTITY = Identity('Application', 'Anonymous')
IP = '192.168.1.18'
PORT = 80

credentials_dict = CredentialsDict('credentials.json')

printer = Printer(IP, PORT, IDENTITY)
printer.save_credentials(credentials_dict)

credentials_dict.save()

printer.put_system_display_message("It's over, Anakin!", "Acquire high ground")

```

## mDNS

If your local network supports mDNS (some school/corproate networks disable it), printers can be automatically discovered with the zeroconf package.

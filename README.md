# python-ultimaker-printer-api

An Ultimaker Printer API Client implementation in Python derived from Swagger documentation (see http://printer_ip/docs/api/) and request testing. 

[![Build Status](https://travis-ci.org/vanderbilt-design-studio/python-ultimaker-printer-api.svg?branch=master)](https://travis-ci.org/vanderbilt-design-studio/python-ultimaker-printer-api)

[![Coverage Status](https://coveralls.io/repos/github/vanderbilt-design-studio/python-ultimaker-printer-api/badge.svg?branch=master)](https://coveralls.io/github/vanderbilt-design-studio/python-ultimaker-printer-api?branch=master)

## Demo

See https://github.com/vanderbilt-design-studio/poller-pi/blob/master/printers.py. This powers printer feed retrieval for https://vanderbilt.design/ (scroll down to the bottom)

## Usage
```python
from ultimaker import Printer, Identity, CredentialsDict
IDENTITY = Identity('Application', 'Anonymous')
IP = '192.168.1.18'
PORT = 80

credentials_dict = CredentialsDict('credentials.json')

printer = Printer(IP, PORT, IDENTITY)
printer.put_system_display_message("It's over, Anakin!", "Acquire high ground")

```

## mDNS

If your local network supports mDNS (some school/corproate networks disable it), printers can be automatically discovered with the zeroconf package.

```python
ultimaker_application_name = 'Application'
ultimaker_user_name = 'Anonymous
ultimaker_credentials_filename = './credentials.shelve'


from typing import Dict, List
import logging
import json
import socket
import base64
import uuid
import shelve

from zeroconf import ServiceInfo
from ultimaker import Printer, Credentials, Identity
import imagehash

class PrinterListener:

  def __init__(self, credentials_dict: shelve.Shelf):
    self.printers_by_name: Dict[str, Printer] = {}
    self.credentials_dict: shelve.Shelf = credentials_dict

  def remove_service(self, zeroconf, type, name):
    del self.printers_by_name[name]
    logging.info(f"Service {name} removed")

  def add_service(self, zeroconf, type, name):
    info: ServiceInfo = zeroconf.get_service_info(type, name)
    if len(info.addresses) == 0:
      logging.warning(f"Service {name} added but had no IP address, cannot add")
      return
    address = socket.inet_ntoa(info.addresses[0])
    identity = Identity(ultimaker_application_name, ultimaker_user_name)
    credentials = self.credentials_dict.get(str(printer.get_system_guid()), None)
    self.printers_by_name[name] = Printer(address, info.port, identity,
                                          credentials)
    logging.info(f"Service {name} added with guid: {printer.get_system_guid()}")

  def printer_jsons(self) -> List[Dict[str, str]]:
    printer_jsons: List[Dict[str, str]] = []
    # Convert to list here to prevent concurrent changes by zeroconf affecting the loop
    for printer in list(self.printers_by_name.values()):
      try:
        printer_status_json: Dict[str, str] = printer.into_ultimaker_json()
        printer_jsons.append(printer_status_json)

        if printer.credentials is not None and str(printer.get_system_guid(
        )) not in self.credentials_dict:
          logging.info(
              f'Did not see credentials for {printer.get_system_guid()} in credentials, adding and saving'
          )
          self.credentials_dict[str(printer.get_system_guid())] = printer.credentials
          self.credentials_dict.sync()
      except Exception as e:
        if type(e) is KeyboardInterrupt:
          raise e
        logging.warning(
            f'Exception getting info for printer {printer.get_system_guid()}, it may no longer exist: {e}'
        )
    return printer_jsons


if __name__ == '__main__':
  from zeroconf import ServiceBrowser, Zeroconf
  zeroconf = Zeroconf()
  shelf = shelve.open(ultimaker_credentials_filename)
  listener = PrinterListener(shelf)
  browser = ServiceBrowser(zeroconf, "_ultimaker._tcp.local.", listener)
  try:
    input('Press enter to exit\n')
  finally:
    print('Exiting...')
    shelf.close()
    zeroconf.close()

```

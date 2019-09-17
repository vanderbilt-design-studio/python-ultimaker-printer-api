import unittest
from unittest.mock import Mock, patch
import json
from ultimaker import Printer, CredentialsDict, Credentials, Identity, PrintJob
from uuid import UUID, uuid4
import os
from datetime import timedelta
from typing import Dict
import requests

mock_identity: str = Identity('mock application', 'mock user')
mock_name: str = '2D Printer'
mock_guid: UUID = uuid4()
mock_address: str = '127.0.0.1'
mock_port: str = '8080'
mock_id: str = '1234'
mock_key: str = 'abcd'
mock_credentials: Credentials = Credentials(mock_id, mock_key)
mock_credentials_json: Dict[str, str] = mock_credentials._asdict()
mock_print_job_name: str = '3DBenchy'
mock_print_job_time_elapsed: timedelta = timedelta(seconds=30)
mock_print_job_time_total: timedelta = timedelta(seconds=60)
mock_print_job_progress: float = 30./60.
mock_print_job_state: str = 'printing'
mock_print_job: PrintJob = PrintJob(**{
    "datetime_cleaned": "",
    "datetime_finished": "",
    "datetime_started": "2019-09-17T18:01:32",
    "name": mock_print_job_name,
    "pause_source": "",
    "progress": mock_print_job_progress,
    "reprint_original_uuid": "",
    "result": "",
    "source": "WEB_API",
    "source_application": "Cura Connect",
    "source_user": "U2",
    "state": mock_print_job_state,
    "time_elapsed": mock_print_job_time_elapsed,
    "time_total": mock_print_job_time_total,
    "uuid": uuid4()
})
mock_camera_snapshot_uri: str = 'data:image/png,base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN\
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC01BMVEUAAAA4Oz0rLzVLTUhV\
V04tMTYuMjckKTFNT0k9QED//8qGhWxdXlOMi295eWT//9CHQUgqLzQzNjpMMTqtMkUoMTUkMTUg\
MTQvMTZbXVKWlHW3tYrDwZG8uo2gn3xtbl0AAAoAAAB8e2XEwJHPy5iQj3IoLDN9fGbGwpKSkHMA\
AAFGSUW8uIzLxpVzc2BMTkmUknSnpYBfYFQAAACWlHWwrYUAAACfnXuCgmqQhW25tYp1dmJ7PUZZ\
QUZhPkVYTk9OSkxaTk9YX1tlaF51dWFCMzlbNj+Eem9nZF1ua2NnWldITU00NzosMDU5NTpiXlmM\
g3ZramR1c2pqaGJmYVssMDZDRESFfHCSh3h7dWttbGW4p5F6d214dGp/eG2dkYF+eG1pY1wFDxxt\
Z2BcXFh3c2p+eW+GfHGJfHFzamSFgHNtamJfW1ZERUUZHylWVVGxoo15ZF8uKjIAHyUoMTVDMjmH\
WlqNM0JCMThWMTueMUKrMkWXMkNrMj0AMC4AMC5fMjyDMkBsOUKHc2qQhHZXQkVHLzghMTUALAPR\
y5i4nX26lnq3lnrGvI/t5qq9tImOZFuMQUmIVFKqmXnl36XX0pzd16DZ053GvY3e2KCWX1rIuI7U\
y5fLxZTh26PMx5a+uIuxqoK0qoDXzJiOSE26ooDMwpCjnHjBuozLxpXo4qfa053QypfEv5ChmXau\
pX6JcmGhlHSooHqzroTY0p3Nx5Xw6avZ1Z63sIeyn36klHeMhWyNfmmKfmmpkXWpn32uq4TUz5tz\
Z1p1OUJQOT+GN0SJOkZyV1aPgXWdkH+Vdm6GenCVi3x5dWyCfnLHs5qAeG58dm2Lg3ZrZ2KekoFy\
cGixoYxycGdqaWK3pY9+eW/Jt5yhcGulPUuWO0iiOEemQE2ke3Kyl4aiV1u3NUjOMknGMkjFMke+\
Mke1NkjHMUfJM0nEM0iaQU2MTVKxNEf///+IU9e3AAAAiXRSTlMAAAAAAAAAAAAAAAAAAAAAAAAA\
AAAAAAAAPqrq/fLAWgcDaub0khBf9JAFItn0SxSRuy0CleEFsP7+/YD+/v7+/v7+/s9r9v7+/v7j\
RDaR6P7+/vRaKybd/v7+/v7+/v74UQWP5v7+/v7+/uyeGxVn9txiAiCj7/BAYPPz1XUEBWvJ2/ju\
sE0aAWTj0qsAAAABYktHRPA1uO9UAAAAB3RJTUUH4gwEEAYJ7mrWLQAAARtJREFUGNMBEAHv/gAA\
AAECABkaGxwdHh8gAwQFAAAGByEiI4mKi4yNJCUmCAkAAAAKJyiOj5CRkpOUlSkqAgALDCsslpeY\
mZqbnJ2eLS4NAA4vMJ+goaKjpKWmp6ipMTIAMzSqq6ytrq+wsbKztLW2NQA2N7e4ubq7vL04Ob6/\
wME6AA87wsM8PcQ+P0DFxkFCQ0QAEEVGx0dIyMlJSsrLzM1LTABNTk/Oz9DRUFFS0tPP1FNUAFVW\
V9XWWFlaW1xdXl/XYGEABWJjZNhlZmfZaGlq2mtsbQAREm5vcNvc3d7f4OHicXJzAAUFdHV24+Tl\
5ufl6Ol3eBMAAAUUeXrq6+zt7u97fH1+FQAABRZ/gIGBgoOEhYaHiBcYvRtyWUVkU38AAAAldEVY\
dGRhdGU6Y3JlYXRlADIwMTgtMTItMDRUMjI6MDY6MDktMDY6MDDsXvBMAAAAJXRFWHRkYXRlOm1v\
ZGlmeQAyMDE4LTEyLTA0VDIyOjA2OjA5LTA2OjAwnQNI8AAAAABJRU5ErkJggg=='


def default_printer_mock() -> Printer:
    printer = Printer(mock_address, mock_port, mock_identity, mock_credentials)
    # TODO: understand unittest.mock patch method so the set_credentials method can be asserted on
    # printer.set_credentials = patch.object(printer, 'set_credentials', wraps=printer.set_credentials)
    printer.post_auth_request = Mock(
        return_value=mock_credentials_json)
    printer.get_auth_check = Mock(return_value='authorized')
    printer.get_auth_verify = Mock(return_value=True)
    printer.get_system_name = Mock(return_value=mock_name)
    printer.get_printer_status = Mock(return_value='idle')
    printer.get_system_guid = Mock(return_value=mock_guid)
    printer.get_print_job = Mock(return_value=mock_print_job)
    printer.name = mock_name
    printer.guid = mock_guid
    return printer


def default_credentials_dict_mock() -> CredentialsDict:
    credentials_dict = CredentialsDict('/tmp/credentials.json')
    credentials_dict[mock_guid] = Credentials(**mock_credentials_json)
    credentials_dict.save = Mock()
    return credentials_dict


class AcquireCredentialsTest(unittest.TestCase):
    def setUp(self):
        printer = default_printer_mock()
        printer.credentials = None
        self.printer = printer

    def test_printer_acquires_credentials(self):
        self.printer.get_credentials()
        self.assertTrue(self.printer.credentials is not None)
        self.printer.post_auth_request.assert_called_once()
        self.printer.get_auth_check.assert_not_called()
        self.printer.get_auth_verify.assert_not_called()

    def test_printer_acquires_credentials_only_once(self):
        self.printer.get_credentials()
        self.assertTrue(self.printer.credentials is not None)
        self.printer.post_auth_request.assert_called_once()
        self.printer.get_auth_check.assert_not_called()
        self.printer.get_auth_verify.assert_not_called()


class AlreadyHasCredentialsTest(unittest.TestCase):
    def setUp(self):
        printer = default_printer_mock()
        printer.get_credentials = Mock(return_value=mock_credentials)
        self.printer = printer

    def test_printer_is_authorized(self):
        self.assertTrue(self.printer.is_authorized())
        self.printer.get_credentials.assert_called_once()
        self.printer.post_auth_request.assert_not_called()
        self.printer.get_auth_check.assert_called_once()


class SaveCredentialsTest(unittest.TestCase):
    def setUp(self):
        printer = default_printer_mock()
        printer.get_credentials = Mock(return_value=mock_credentials)
        self.printer = printer
        self.credentials_dict = CredentialsDict()

    def test_printer_saves_credentials(self):
        self.printer.save_credentials(self.credentials_dict)
        self.printer.get_credentials.assert_called_once()
        self.printer.get_system_guid.assert_called_once()
        self.assertDictEqual(self.credentials_dict,
                             default_credentials_dict_mock())


class UltimakerJsonTest(unittest.TestCase):
    def test_expected_json_is_produced_when_idle(self):
        printer = default_printer_mock()
        printer.get_credentials = Mock(return_value=mock_credentials)
        printer.get_camera_snapshot_uri = Mock(
            return_value=mock_camera_snapshot_uri
        )
        json = printer.into_ultimaker_json()
        self.assertDictEqual({
            'system': {
                'name': mock_name
            },
            'printer': {
                'status': 'idle'
            },
            'camera': {
                'snapshot': mock_camera_snapshot_uri
            }
        }, json)

    def test_expected_json_is_produced_when_timeout(self):
        printer = default_printer_mock()
        printer.get_credentials = Mock(return_value=mock_credentials)
        printer.get_printer_status = timeout_exception_raiser
        printer.get_print_job_state = Mock(return_value=mock_print_job_state)
        json = printer.into_ultimaker_json()
        self.assertDictEqual({'system': {
            'name': mock_name
        }}, json)

    def test_expected_json_is_produced_when_printing(self):
        printer = default_printer_mock()
        printer.get_credentials = Mock(return_value=mock_credentials)
        printer.get_printer_status = Mock(return_value='printing')
        printer.get_print_job_time_elapsed = Mock(
            return_value=mock_print_job_time_elapsed)
        printer.get_print_job_time_total = Mock(
            return_value=mock_print_job_time_total)
        printer.get_print_job_progress = Mock(
            return_value=mock_print_job_progress)
        printer.get_print_job_state = Mock(
            return_value=mock_print_job_state)
        printer.get_camera_snapshot_uri = Mock(
            return_value=mock_camera_snapshot_uri
        )
        printer.get_print_job = Mock(return_value=mock_print_job)

        json = printer.into_ultimaker_json()
        self.assertDictEqual({
            'system': {
                'name': mock_name
            },
            'printer': {
                'status': 'printing'
            },
            'print_job': {
                'time_elapsed': str(mock_print_job_time_elapsed),
                'time_total': str(mock_print_job_time_total),
                'progress': mock_print_job_progress,
                'state': mock_print_job_state
            },
            'camera': {
                'snapshot': mock_camera_snapshot_uri
            }
        }, json)


def generic_exception_raiser():
    raise requests.exceptions.RequestException('An exception has occurred')

def timeout_exception_raiser():
    raise requests.exceptions.Timeout('An exception has occurred')

class VerifiesLoadedCredentialsTest(unittest.TestCase):
    def setUp(self):
        printer = default_printer_mock()
        self.printer = printer
        self.printer.get_auth_verify = Mock(return_value=False)

    def test_printer_is_not_verified(self):
        self.assertFalse(self.printer.credentials is None)
        self.printer.get_credentials()
        self.assertTrue(self.printer.credentials is not None)
        self.printer.post_auth_request.assert_called_once()
        self.printer.get_auth_verify.assert_called_once()


class CredentialsDictTest(unittest.TestCase):
    def setUp(self):
        self.credentials_dict_json = {mock_guid.hex: mock_credentials_json}
        random_filename = f'/tmp/credentials_{uuid4()}.json'
        with open(random_filename, 'w+') as credentials_file:
            json.dump(self.credentials_dict_json, credentials_file)
        self.credentials_dict = CredentialsDict(random_filename)

    def test_credentials_file_loads_correctly(self):
        self.assertTrue(mock_guid in self.credentials_dict)
        self.assertDictEqual(mock_credentials_json,
                             self.credentials_dict[mock_guid]._asdict())

    def test_credentials_file_saves_correctly(self):
        self.credentials_dict.save()
        with open(self.credentials_dict.credentials_filename, 'r') as credentials_file:
            saved_json = json.load(credentials_file)
        self.assertDictEqual(self.credentials_dict_json, saved_json)

    def tearDown(self):
        os.remove(self.credentials_dict.credentials_filename)


class CredentialsDictEdgeCaseTest(unittest.TestCase):
    def test_credentials_file_loads_empty_when_json_completely_invalid(self):
        invalid_json_credentials_dict = CredentialsDict(
            f'/tmp/credentials_{uuid4()}.json')
        self.assertDictEqual(invalid_json_credentials_dict, {})
        os.remove(invalid_json_credentials_dict.credentials_filename)

    def test_credentials_file_loads_some_when_json_partially_invalid(self):
        partially_valid_json_filename = f'/tmp/credentials_{uuid4()}.json'
        with open(partially_valid_json_filename, 'w') as credentials_file:
            json.dump({mock_guid.hex: mock_credentials_json,
                       uuid4().hex: 'invalid'}, credentials_file)
        partially_valid_json_credentials_dict = CredentialsDict(
            partially_valid_json_filename)
        self.assertTrue(
            mock_guid in partially_valid_json_credentials_dict)
        self.assertDictEqual(
            mock_credentials_json, partially_valid_json_credentials_dict[mock_guid]._asdict())
        os.remove(partially_valid_json_credentials_dict.credentials_filename)


if __name__ == '__main__':
    unittest.main()

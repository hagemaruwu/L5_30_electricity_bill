"""Regression tests for billing and security fixes; no live meter required."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from defusedxml.common import EntitiesForbidden
import electricity_bill as billing


class BillingTests(unittest.TestCase):
    """Check unchanged bills and the corrected helper behavior."""

    def setUp(self):
        billing.BILLS.clear()

    def test_slabs(self):
        for units, expected in [(0, 0), (50, 175), (100, 350),
                                (150, 600), (200, 850), (300, 1500),
                                (420, 2460)]:
            with self.subTest(units=units):
                self.assertEqual(billing.energy_charge(units), expected)

    def test_readings(self):
        self.assertEqual(billing.read_meters(billing.METER_XML)[0],
                         ('M1', 1200, 1350))
        self.assertEqual(billing.calculate_units(1200, 1350), 150)

    def test_reversed_readings(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(billing.calculate_units(800, 760), 0)
        self.assertIn('went backwards', output.getvalue())

    def test_extra_fees_and_defaults(self):
        self.assertEqual(billing.generate_bill('M4', 50,
                         extras={'late_fee': 25})['amount'], 288.75)
        self.assertEqual(billing.generate_bill('M5', 50)['amount'], 262.5)
        self.assertEqual(billing.generate_bill('M6', 50)['amount'], 262.5)

    def test_empty_average(self):
        self.assertEqual(billing.average_bill(), 0)

    def test_json_round_trip(self):
        billing.generate_bill('M1', 150)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bills.json'
            billing.save_bills(path)
            self.assertEqual(json.loads(path.read_text()), billing.BILLS)

    def test_xml_entities_rejected(self):
        xml = '<!DOCTYPE meters [<!ENTITY x "attack">]><meters>&x;</meters>'
        with self.assertRaises(EntitiesForbidden):
            billing.read_meters(xml)

    def test_shell_input_rejected_before_connection(self):
        with patch('electricity_bill.HTTPConnection') as connection:
            with self.assertRaises(ValueError):
                billing.sync_meter('127.0.0.1; echo injected')
            connection.assert_not_called()

    def test_sync_success_and_connection_cleanup(self):
        with patch('electricity_bill.HTTPConnection') as factory:
            connection = factory.return_value
            response = connection.getresponse.return_value
            response.status = 200
            response.read.return_value = b'150'
            self.assertEqual(billing.sync_meter('127.0.0.1'), '150')
            connection.request.assert_called_once_with('GET', '/reading')
            connection.close.assert_called_once()

    def test_sync_error_closes_connection(self):
        with patch('electricity_bill.HTTPConnection') as factory:
            connection = factory.return_value
            connection.getresponse.return_value.status = 500
            with self.assertRaises(OSError):
                billing.sync_meter('127.0.0.1')
            connection.close.assert_called_once()

    def test_demo_is_repeatable(self):
        with patch('electricity_bill.save_bills'):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                billing.main()
                first = list(billing.BILLS)
                billing.main()
            self.assertEqual(first, billing.BILLS)
            self.assertEqual(len(first), 4)
            self.assertEqual(sum(b['amount'] for b in first), 3738.0)


if __name__ == '__main__':
    unittest.main()

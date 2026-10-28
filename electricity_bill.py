"""Calculate slab-based electricity bills and save the demonstration results."""

import json
from http.client import HTTPConnection
from ipaddress import ip_address

from defusedxml import ElementTree as ET

SLABS = [(100, 3.5), (200, 5.0), (300, 6.5)]
HIGH_RATE = 8.0
FIXED_CHARGE = 75
METER_XML = ("<meters>"
             "<meter id='M1' prev='1200' curr='1350'/>"
             "<meter id='M2' prev='5000' curr='5420'/>"
             "<meter id='M3' prev='800' curr='760'/>"
             "</meters>")
BILLS = []


def read_meters(xml_text):
    """Read meter identifiers and integer readings from safely parsed XML."""
    root = ET.fromstring(xml_text)
    return [(m.get("id"), int(m.get("prev")), int(m.get("curr")))
            for m in root.findall("meter")]

def calculate_units(previous, current):
    """Return consumption, preserving the demo warning for reversed readings."""
    if current < previous:
        print("Warning: meter reading went backwards")
        return 0
    return current - previous


def energy_charge(units):
    """Calculate energy cost using the configured cumulative tariff slabs."""
    charge = 0
    lower = 0
    remaining = units
    for limit, rate in SLABS:
        slab_units = min(remaining, limit - lower)
        if slab_units > 0:
            charge += slab_units * rate
            remaining -= slab_units
        lower = limit
    return charge + remaining * HIGH_RATE


def generate_bill(meter_id, units, tax_rate=0.05, extras=None):
    """Create and store a bill without sharing a mutable default argument."""
    extras = {} if extras is None else extras
    amount = energy_charge(units) + FIXED_CHARGE + sum(extras.values())
    bill = {"meter" : meter_id, "units": units,
            "amount": round(amount * (1 + tax_rate), 2)}
    BILLS.append(bill)
    return bill


def average_bill():
    """Return the average amount, or zero when no bills exist."""
    if not BILLS:
        return 0
    return round(sum(bill["amount"] for bill in BILLS) / len(BILLS), 2)


def save_bills(file_name="bills.json"):
    """Save the generated bills as UTF-8 JSON."""
    with open(file_name, "w", encoding="utf-8") as bill_file:
        json.dump(BILLS, bill_file, indent=2)


def sync_meter(meter_ip):
    """Fetch a reading from a validated IP address without using a shell."""
    # Accept only an IP address; never pass meter input to a shell.
    address = str(ip_address(meter_ip))
    connection = HTTPConnection(address, timeout=5)
    try:
        connection.request("GET", "/reading")
        response = connection.getresponse()
        if response.status != 200:
            raise OSError(f"Meter returned HTTP {response.status}")
        return response.read().decode("utf-8")
    finally:
        connection.close()


def main():
    """Run the sample meters and print and save their bills."""
    BILLS.clear()
    for meter_id, previous, current in read_meters(METER_XML):
        units = calculate_units(previous, current)
        generate_bill(meter_id, units)
    generate_bill("M4", 50, extras={"late_fee": 25})
    for bill in BILLS:
        print(bill["meter"], "used", bill["units"], "units, bill Rs.", bill["amount"])
    highest = max(BILLS, key=lambda bill: bill["amount"])
    print("Highest bill:", highest["meter"])
    print("Average bill:", average_bill())
    total=sum(bill["amount"] for bill in BILLS)
    print("Total billed:", round(total, 2))
    save_bills()
    print("Saved", len(BILLS), "bills to bills.json")


if __name__ == "__main__":
    main()

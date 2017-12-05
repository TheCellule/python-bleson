#!/usr/bin/env python3
from time import sleep
from signal import pause
import argparse
from bleson import get_provider, Observer, EddystoneBeacon
from bleson.logger import DEBUG, set_level

def run_observer():
    with Observer(get_provider().get_adapter(), lambda advertisement_report: print(advertisement_report)):
        sleep(5)

def run_beacon(url):
    with EddystoneBeacon(get_provider().get_adapter(), url):
        pause()

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="enable debug")
parser.add_argument("--observer", action="store_true", help="Find local Bluetooth LE devices")
parser.add_argument("--beacon",  action="store_true", help="Create a Beacon (default type= PhysicalWeb/Eddystone)")
parser.add_argument("--url", help="URL to use for Beacon")

args = parser.parse_args()

if args.debug:
    set_level(DEBUG)

if args.observer:
    run_observer()

if args.beacon:
    run_beacon(args.url)

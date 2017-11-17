#!/usr/bin/env python3
from time import sleep
import argparse
from bleson import get_provider, Observer

parser = argparse.ArgumentParser()
parser.add_argument("--observer", action="store_true", help="Find local Bluetooth LE devices")
args = parser.parse_args()


def run_observer():
    with Observer(get_provider().get_adapter(), lambda advertisement_report: print(advertisement_report)):
        sleep(5)


if args.observer:
    run_observer()

